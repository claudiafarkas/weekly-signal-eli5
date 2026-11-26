from pathlib import Path

import pytest

from weekly_signal.ingestion import load_source_addresses

FIXTURES = Path(__file__).parent / "fixtures"
ROOT = Path(__file__).resolve().parents[1]


def test_load_sources_reads_enabled_and_paused_publishers() -> None:
    sources = load_source_addresses(FIXTURES / "sources.yaml")

    assert [source.id for source in sources] == ["example", "paused"]
    assert sources[0].enabled is True
    assert sources[1].enabled is False
    assert str(sources[0].url) == "https://example.com/rss"


def test_load_sources_rejects_an_entry_missing_a_url() -> None:
    with pytest.raises(ValueError, match="invalid"):
        load_source_addresses(FIXTURES / "sources_invalid.yaml")


def test_project_source_list_loads() -> None:
    sources = load_source_addresses(ROOT / "config" / "sources.yaml")
    enabled_ids = {source.id for source in sources if source.enabled}

    assert "the-verge" in enabled_ids
    assert "hacker-news" in enabled_ids
    assert all(source.kind == "rss" for source in sources)
