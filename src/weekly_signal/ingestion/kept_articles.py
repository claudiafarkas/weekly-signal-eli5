"""Keep this week's stories and drop repeats.

The download step returns every item in a feed. This step only decides which
of those items are recent and which article ids have already been kept. It
does not download anything, and it does not call a model.
"""

from datetime import datetime, timedelta, timezone

from weekly_signal.models import Article

LOOKBACK_DAYS = 8


def keep_recent_articles(
    articles: list[Article],
    *,
    now: datetime | None = None,
    lookback_days: int = LOOKBACK_DAYS,
) -> list[Article]:
    """Keep stories from the last lookback_days, one copy of each article_id.

    A story with no published_at is dropped. The first copy of an article_id
    is kept and later copies are dropped. Pass now in tests so the cutoff
    does not depend on the clock.
    """
    moment = now or datetime.now(timezone.utc)
    cutoff = moment - timedelta(days=lookback_days)
    kept: list[Article] = []
    seen: set[str] = set()
    for article in articles:
        published_at = article.published_at
        if published_at is None or published_at < cutoff:
            continue
        if article.article_id in seen:
            continue
        seen.add(article.article_id)
        kept.append(article)
    return kept
