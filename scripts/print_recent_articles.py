"""Download enabled feeds and print how many stories are from the last 8 days.

Reading the publisher list happens in load_source_addresses. Downloading one
feed happens in download_source_content. Choosing which stories to keep
happens in kept_articles. This file only calls those three and prints.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weekly_signal.ingestion.download_source_content import download_source_content  # noqa: E402
from weekly_signal.ingestion.kept_articles import keep_recent_articles  # noqa: E402
from weekly_signal.ingestion.load_source_addresses import load_source_addresses  # noqa: E402


def main() -> None:
    sources = load_source_addresses(ROOT / "config" / "sources.yaml")
    articles = []
    for source in sources:
        if source.enabled:
            articles.extend(download_source_content(source))
    kept = keep_recent_articles(articles)
    print(f"downloaded {len(articles)}")
    print(f"kept {len(kept)}")
    print(f"dropped {len(articles) - len(kept)}")
    print()
    for article in kept[:10]:
        published = article.published_at.strftime("%Y-%m-%d")
        print(f"{published}  {article.publisher}  {article.title}")


if __name__ == "__main__":
    main()
