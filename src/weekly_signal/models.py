"""Shapes the pipeline passes from one stage to the next.

A Source is one publisher from config/sources.yaml. An Article is one story
taken from that publisher's feed.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class Source(BaseModel):
    """One configured publisher.

    `kind` is only "rss" for now. A new access method, such as the Hacker News
    API, gets its own value here instead of a special case buried in the fetcher.
    """

    id: str = Field(min_length=1, pattern=r"^[a-z0-9-]+$")
    publisher: str = Field(min_length=1)
    kind: Literal["rss"]
    url: HttpUrl
    enabled: bool = True


class Article(BaseModel):
    """One story from a feed. Built from feed fields only."""

    article_id: str
    source_id: str
    publisher: str
    title: str
    url: str
    published_at: datetime | None = None
    description: str | None = None
    content_excerpt: str | None = None
