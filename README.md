# CurrencyLens

A small ETL + AI project that tracks currency exchange rates over time, analyses trends, and generates
plain-language summaries of what's happening in the market.

## About this project

This project is being built by me, **Mário Rosa**, as a hands-on way to deepen my skills in data
pipelines, testing, CI/CD, and applied AI. I'm building it with the support of **Claude (Anthropic)**
as a mentor — Claude explains concepts, reviews my code, and helps me structure the work, but the
implementation decisions and the code itself are mine. Where I got stuck and asked for a solution
directly, that's noted in the relevant commit or file.

This is a companion project to [HomeBase](#), which I'm also building with AI support, on a slower
timeline. CurrencyLens is meant to be smaller and faster to complete, while still being genuinely
useful for my portfolio.

## What it does

1. **Extract** — pulls daily exchange rates for a set of currency pairs from the
   [Frankfurter API](https://www.frankfurter.app/) (free, no API key required).
2. **Load** — stores each day's rates in a local SQLite database, building a history over time.
3. **Analyse** — uses Pandas to calculate day-over-day and week-over-week changes, and moving
   averages, once enough data has accumulated.
4. **Summarise** — calls an AI model (Claude or OpenAI) to turn the numbers into a short, readable
   summary of what happened and why it might matter.
5. **Test & automate** — the whole pipeline is covered by unit tests (Pytest) and runs automatically
   every day via GitHub Actions, which also run the test suite on every push.

## Why I'm building this

I wanted a project that was realistic to finish in a week or two (unlike HomeBase, which is a longer
build), while still covering real gaps in my portfolio: authoring my own CI/CD pipeline, working with
data end-to-end (not just consuming an API once), and actually calling an AI model from my own code —
as opposed to using AI tools as a coding assistant, which is a different skill.

## Status

🚧 In progress. See [PROGRESS.md](./PROGRESS.md) for a session-by-session log of what's been done.

## Tech stack

- Python 3.11+
- SQLite (via the standard library `sqlite3`)
- Pandas
- Pytest
- GitHub Actions
- Claude or OpenAI API (for the summary step)
- (Optional, later) Streamlit for a small dashboard

## Project structure

CurrencyLens is organised as a single Python package (`currencylens/`), with one module per stage of
the pipeline described above, plus a `tests/` folder mirroring it one-to-one:

```
CurrencyLens/
├── currencylens/
│   ├── __init__.py       # makes this folder an importable package
│   ├── config.py         # settings: currency pairs to track, file paths, etc.
│   ├── fetch_rates.py    # Extract — calls the Frankfurter API
│   ├── database.py       # Load — reads/writes the SQLite database
│   ├── analysis.py       # Analyse — Pandas calculations (changes, moving averages)
│   ├── summarize.py      # Summarise — calls the AI model
│   └── main.py           # orchestrates the pipeline end to end
├── tests/
│   ├── test_fetch_rates.py
│   ├── test_database.py
│   ├── test_analysis.py
│   └── test_summarize.py
├── .gitignore
├── requirements.txt
├── README.md
├── PROGRESS.md
└── SESSION_CHECKLIST.md
```

Each pipeline stage is its own module so it can be tested independently (e.g. testing the Pandas
calculations in `analysis.py` doesn't require a real database or a real API call). `main.py` is the
only place that ties the stages together and is the entry point for actually running the pipeline.

I considered the stricter "src layout" (`src/currencylens/` + a `pyproject.toml` to make the package
properly installable) that's common in production Python projects, but decided against it for now:
CurrencyLens isn't published as a library for other projects to depend on, it's a standalone script
run via cron in GitHub Actions, so the extra packaging ceremony wasn't worth it. This structure can be
migrated to a src layout later if the project ever needs it.

## Setup

1. Clone the repository and `cd` into it.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the pipeline (once `main.py` exists):
   ```
   python -m currencylens.main
   ```

## License

MIT — feel free to use this as a reference, but it's a learning project, not a production tool.
