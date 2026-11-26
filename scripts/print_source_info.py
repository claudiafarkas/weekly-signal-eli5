"""Print the publishers from config/sources.yaml.

Run this when you want to see the list, or to find out that an entry is
invalid. Reading the file and checking each publisher happens in
weekly_signal.ingestion.load_source_addresses. Nothing is stored in a database.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weekly_signal.ingestion import load_source_addresses  # noqa: E402


def main() -> None:
    sources = load_source_addresses(ROOT / "config" / "sources.yaml")
    enabled = [source for source in sources if source.enabled]
    print(f"{len(enabled)} enabled, {len(sources) - len(enabled)} paused")
    for source in enabled:
        print(f"- {source.publisher}  {source.url}")


if __name__ == "__main__":
    main()
