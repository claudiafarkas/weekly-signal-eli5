from pathlib import Path

import httpx

from weekly_signal.ingestion.download_source_content import (
    articles_from_feed,
    download_source_content,
)
from weekly_signal.models import Source

FIXTURES = Path(__file__).parent / "fixtures"
SOURCE = Source(
    id="example",
    publisher="Example Times",
    kind="rss",
    url="https://example.com/rss",
)


def test_articles_from_feed_keeps_the_story_and_drops_the_untitled_item() -> None:
    xml = (FIXTURES / "sample_feed.xml").read_text(encoding="utf-8")

    articles = articles_from_feed(SOURCE, xml)

    assert len(articles) == 1
    article = articles[0]
    assert article.title == "A real story"
    assert article.url == "https://example.com/story?utm_source=rss"
    assert article.publisher == "Example Times"
    assert article.source_id == "example"
    assert article.description == "Short description."
    assert article.content_excerpt == "The feed body."
    assert article.published_at is not None
    assert article.published_at.year == 2026


def test_article_id_ignores_tracking_parameters() -> None:
    xml = (FIXTURES / "sample_feed.xml").read_text(encoding="utf-8")
    other = xml.replace("utm_source=rss", "utm_source=email")

    first = articles_from_feed(SOURCE, xml)[0]
    second = articles_from_feed(SOURCE, other)[0]

    assert first.article_id == second.article_id


def test_failed_download_returns_no_articles(monkeypatch) -> None:
    def explode(url: str) -> str:
        raise httpx.ConnectError("feed is down")

    monkeypatch.setattr(
        "weekly_signal.ingestion.download_source_content._download_feed",
        explode,
    )

    assert download_source_content(SOURCE) == []
