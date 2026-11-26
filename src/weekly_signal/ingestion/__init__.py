"""Load the publisher list. Feed downloads live in download_source_content.py. The 8-day filter lives in kept_articles.py."""

from weekly_signal.ingestion.load_source_addresses import load_source_addresses

__all__ = ["load_source_addresses"]
