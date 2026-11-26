# The Weekly Signal

Less noise. More signal.

This page describes the pipeline as the files work today. A run reads the publisher list, downloads each enabled feed, and keeps the stories from the last 8 days.

## Run

`scripts/print_recent_articles.py` is the command for this stage. It calls three library functions, in order. Those functions live in `src/weekly_signal/ingestion/`. They wait to be called. They do not call each other, and they are not scripts.

```text
config/sources.yaml
        │
        ▼
load_source_addresses          Source records: who to read, and where
        │
        ▼
download_source_content        Article records: one story per feed item
        │
        ▼
keep_recent_articles           the same articles, minus old and repeated ones
        │
        ▼
print counts, then 10 titles
```

`scripts/print_source_info.py` is a separate command. It calls only `load_source_addresses` and prints each publisher with its feed URL. Use it to check the list without downloading.

## Publishers

`config/sources.yaml` is the list of sites. Each entry is one publisher:

| Field | Meaning |
| --- | --- |
| `id` | Short name used in code, such as `the-verge` |
| `publisher` | Name printed in the letter |
| `kind` | `rss` for every source so far |
| `url` | The feed address |
| `enabled` | `false` leaves the publisher in the file and skips the download |

The pipeline does not hard-code these sites. Adding or removing a publisher is an edit to this file.

## Library

### `load_source_addresses`

File: `src/weekly_signal/ingestion/load_source_addresses.py`

Reads `config/sources.yaml` and returns `Source` records, including publishers that are turned off. A `Source` is an address. It has no title, date, or article body.

The function raises `ValueError` when the file is not a publisher list, an entry is missing a required field, or two entries share an `id`.

### `download_source_content`

File: `src/weekly_signal/ingestion/download_source_content.py`

Takes one `Source` and downloads `source.url`. Each feed item with a title and a link becomes an `Article`:

| Field | Meaning |
| --- | --- |
| `article_id` | First 16 hex characters of the SHA-256 of the normalized URL |
| `source_id` | The publisher's `id` |
| `publisher` | The publisher's name |
| `title` | Story title, tags removed |
| `url` | Link from the feed |
| `published_at` | Publish date in UTC, when the feed gives one |
| `description` | Short summary from the feed |
| `content_excerpt` | Body text, only when the feed includes it, capped at 2000 characters |

The script calls this once per enabled source and stacks the articles into one list. A failed download is logged and returns `[]`, so one publisher does not stop the run. Article pages are not fetched. The body is whatever the feed already supplied.

URL normalization lowercases the host, drops the fragment, and removes `utm_*`, `fbclid`, and `gclid`. The same story with a different tracking parameter keeps the same `article_id`.

### `keep_recent_articles`

File: `src/weekly_signal/ingestion/kept_articles.py`

Takes the combined list. One pass keeps a story when all of these are true:

- `published_at` is present
- `published_at` is within the last 8 days, including a story published exactly 8 days ago
- this `article_id` has not already been kept

The first copy of an id stays. Later copies are dropped. Stories with no date are dropped, because the filter cannot tell whether they belong to this week.

## Records

`src/weekly_signal/models.py` holds the two shapes the pipeline passes along.

**Source** is one publisher from the YAML file: `id`, `publisher`, `kind`, `url`, `enabled`.

**Article** is one story from a feed: `article_id`, `source_id`, `publisher`, `title`, `url`, `published_at`, `description`, `content_excerpt`.

## Checks

`pytest` stays offline.

| Test file | What it checks |
| --- | --- |
| `tests/test_load_sources.py` | The publisher list loads, a bad entry fails, and the real config contains the expected ids |
| `tests/test_download_source_content.py` | A saved feed becomes one article, tracking parameters do not change the id, and a failed download returns nothing |
| `tests/test_keep_recent_articles.py` | Old stories, undated stories, and repeated ids are dropped |
