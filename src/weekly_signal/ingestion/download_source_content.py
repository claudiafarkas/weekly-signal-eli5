"""Download one feed and turn its items into Article records.

The caller already has a Source, including source.url. This module does not
read sources.yaml again, and it does not write to a database.
"""

import hashlib
import logging
import re
from datetime import datetime, timezone
from html import unescape
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import httpx

from weekly_signal.models import Article, Source

logger = logging.getLogger(__name__)

_USER_AGENT = "WeeklySignal/0.1 (personal research newsletter)"
_EXCERPT_LIMIT = 2000
_TAG = re.compile(r"<[^>]+>")
_SPACE = re.compile(r"\s+")


def download_source_content(source: Source) -> list[Article]:
    """Download source.url and return the stories in that feed.

    A failed download or an unreadable feed is logged and returns an empty
    list, so one publisher cannot stop the rest of the run.
    """
    try:
        xml = _download_feed(str(source.url))
        return articles_from_feed(source, xml)
    except (httpx.HTTPError, OSError):
        logger.exception("Feed failed for %s", source.id)
        return []


def articles_from_feed(source: Source, xml: str) -> list[Article]:
    """Parse feed XML that was already downloaded."""
    parsed = feedparser.parse(xml)
    articles: list[Article] = []
    for entry in parsed.entries:
        article = _article_from_entry(source, entry)
        if article is not None:
            articles.append(article)
    return articles


def _download_feed(url: str) -> str:
    response = httpx.get(
        url,
        timeout=15,
        follow_redirects=True,
        headers={"User-Agent": _USER_AGENT},
    )
    response.raise_for_status()
    return response.text


def _article_from_entry(source: Source, entry: feedparser.FeedParserDict) -> Article | None:
    title = _plain_text(entry.get("title"), limit=300)
    link = entry.get("link")
    if not title or not link:
        return None

    raw_body = None
    if entry.get("content"):
        raw_body = entry.content[0].get("value")

    return Article(
        article_id=_article_id(link),
        source_id=source.id,
        publisher=source.publisher,
        title=title,
        url=link,
        published_at=_published_at(entry),
        description=_plain_text(entry.get("summary")),
        content_excerpt=_plain_text(raw_body),
    )


def _article_id(url: str) -> str:
    normalized = _normalize_url(url)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def _normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.startswith("utm_") and key not in {"fbclid", "gclid"}
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def _published_at(entry: feedparser.FeedParserDict) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return None
    return datetime(*parsed[:6], tzinfo=timezone.utc)


def _plain_text(value: str | None, limit: int = _EXCERPT_LIMIT) -> str | None:
    if not value:
        return None
    text = _SPACE.sub(" ", unescape(_TAG.sub(" ", value))).strip()
    if not text:
        return None
    return text[:limit]
