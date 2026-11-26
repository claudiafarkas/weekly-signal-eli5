from datetime import datetime, timedelta, timezone

from weekly_signal.ingestion.kept_articles import keep_recent_articles
from weekly_signal.models import Article

NOW = datetime(2026, 11, 25, 12, tzinfo=timezone.utc)


def _article(article_id: str, *, days_ago: int | None) -> Article:
    published_at = None if days_ago is None else NOW - timedelta(days=days_ago)
    return Article(
        article_id=article_id,
        source_id="example",
        publisher="Example Times",
        title=article_id,
        url=f"https://example.com/{article_id}",
        published_at=published_at,
    )


def test_keeps_a_story_from_this_week_and_drops_an_old_one() -> None:
    recent = _article("recent", days_ago=3)
    old = _article("old", days_ago=9)

    kept = keep_recent_articles([old, recent], now=NOW)

    assert kept == [recent]


def test_keeps_a_story_published_exactly_eight_days_ago() -> None:
    edge = _article("edge", days_ago=8)

    assert keep_recent_articles([edge], now=NOW) == [edge]


def test_drops_a_story_with_no_date() -> None:
    undated = _article("undated", days_ago=None)

    assert keep_recent_articles([undated], now=NOW) == []


def test_keeps_the_first_copy_of_a_repeated_article_id() -> None:
    first = _article("same", days_ago=1)
    second = _article("same", days_ago=2)

    kept = keep_recent_articles([first, second], now=NOW)

    assert kept == [first]
