# The Weekly Signal

Less noise. More signal.

A Sunday letter on technology, data, and business. Python will collect the news, choose what matters, and write the issue. The site collects the addresses that receive it.

## Layout

- `src/weekly_signal/` — the pipeline. `ingestion/load_source_addresses.py` reads the publisher list. `ingestion/download_source_content.py` downloads one feed.
- `scripts/print_source_info.py` — the command that prints that list. Scripts stay thin. The work they call lives in `src/`.
- `config/sources.yaml` — the publisher list. Add or remove a source here.
- `web/` — the landing page, deployed later on Vercel.
- Supabase will hold the hosted list. Render will run the weekly job. Resend will deliver the letter. None of those are connected yet.

## Run the landing page

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

An email submitted on this page is stored in `web/.data/signups.json` on your machine. That file is gitignored. No confirmation email is sent. When `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are set, the form refuses to pretend the hosted list exists until that save is built.

## Pipeline

Use Python 3.12. The landing page does not need it.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python scripts/print_source_info.py
```

`pytest` checks the loader without using the network. The script prints the enabled publishers from `config/sources.yaml`.

Copy `.env.example` to `.env` when the pipeline needs secrets. Do not commit `.env`.
