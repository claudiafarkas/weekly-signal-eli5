"""Read config/sources.yaml into Source records in memory.

print_source_info.py calls load_source_addresses. This file returns the list.
It does not download feeds, it does not print, and it does not write to a database.
"""

from pathlib import Path

import yaml
from pydantic import ValidationError

from weekly_signal.models import Source


def load_source_addresses(path: Path) -> list[Source]:
    """Return every publisher in the file, including disabled ones.

    Raises ValueError when the file is not a publisher list, an entry is
    missing a required field, or two entries share an id.

    this function only knows the addresses of the sources. It does not know the stories in them.
    """
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise ValueError(f"{path} must contain a 'sources' list")

    sources: list[Source] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(raw["sources"], start=1):
        try:
            source = Source.model_validate(entry)
        except ValidationError as error:
            raise ValueError(f"Source {index} in {path.name} is invalid: {error}") from error
        if source.id in seen_ids:
            raise ValueError(f"Duplicate source id: {source.id}")
        seen_ids.add(source.id)
        sources.append(source)
    return sources
