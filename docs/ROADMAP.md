# Roadmap — CurrencyLens

This document is the map of the project, from an empty folder to a daily automated pipeline. Each
phase has:
- **Goal** — what the project can do by the end of the phase
- **What it involves** — the technical pieces to build
- **Done criteria** — how I know it's ready to move on
- **Who writes what** — what I write myself, and where Claude's support comes in

Order matters: each phase builds on the previous one. Every phase also includes the tests for its
own module, written as I go and not left for the end.

The phases map to the epics and sprints on the GitHub Projects board (see `PROJECT_MANAGEMENT.md`).

---

## Phase 0 — Setup (done)
**Goal:** get the machine, GitHub and the project skeleton ready.

What it involves:
- Python, Git and VSCode working; the `CurrencyLens` repository on GitHub
- Virtual environment (`venv`), `.gitignore` and the first `requirements.txt`
- Package scaffold: `currencylens/` (one module per pipeline stage) and `tests/`
- `config.py` with the project's settings

**Done when:** the virtual environment is active, `python -c "from currencylens import config"` runs
without errors, and the repository on GitHub contains the scaffold.

**Who writes what:** the setup was done step by step with Claude's guidance; `config.py` is mine,
reviewed together.

---

## Phase 1 — Extract
**Goal:** fetch the latest exchange rates from the Frankfurter API reliably.

What it involves:
- `fetch_rates.py`: build the request from `config.py` (API URL, base currency, timeout) and call the
  `/latest` endpoint with `requests`
- Turn the JSON response into a clean Python structure (the date plus a dictionary of rates)
- Error handling: timeouts, HTTP error codes and unexpected responses should fail with clear errors
- First `pytest` tests, using a mocked HTTP call so the tests never touch the real network

**Done when:** calling the function returns the latest rates for the configured currencies, and the
tests pass without internet access.

**Who writes what:** I write the fetch function, the error handling and the tests; Claude explains
`requests`, status codes and mocking.

---

## Phase 2 — Load
**Goal:** store each day's rates in SQLite, building a history without duplicates.

What it involves:
- `docs/DATA_MODEL.md`: the table design, written before the code (one row per date and currency,
  with a uniqueness rule)
- `database.py`: connect with the standard library `sqlite3`, create the table, insert rates, and
  read the history back
- Running the pipeline twice on the same day must not create duplicate rows
- `docs/ARCHITECTURE.md`: the pipeline and the data flow, now that two stages exist
- Tests using a temporary database

**Done when:** running Extract and Load twice leaves exactly one row per currency per date, and the
tests pass.

**Who writes what:** I write the schema, the SQL and the functions; Claude explains SQL basics,
constraints and why SQL values are always passed as parameters and never built with string
formatting.

---

## Phase 3 — Analyse
**Goal:** turn the stored rates into trend numbers.

What it involves:
- `analysis.py`: load the history into a Pandas DataFrame
- Day-over-day and week-over-week percentage changes
- Moving averages, using the windows from `config.py`
- Cross rates between any two currencies, derived from the EUR-based rates
- Missing days (weekends, holidays) and too little history, handled without crashing
- Tests using small DataFrames built by hand

**Done when:** one function returns a table of changes and moving averages per currency, and it
behaves sensibly with only a few days of data.

**Who writes what:** I write the Pandas logic and the tests; Claude explains DataFrames, grouping and
rolling windows, and reviews the code for idiomatic Pandas.

---

## Phase 4 — Summarise
**Goal:** an AI-generated, plain-language summary of what happened in the market.

What it involves:
- Choose the provider (Claude or OpenAI) and add its SDK to `requirements.txt`
- The API key goes in `.env` (never committed), with a `.env.example` as a template
- `summarize.py`: build a prompt from the analysis results, call the model, and handle failures
- A prompt that gives the model the real numbers and asks it not to invent causes
- Tests with a mocked client

**Done when:** the pipeline produces a short, readable summary from real data, and no secret appears
anywhere in the repository.

**Who writes what:** I write the prompt, the call and the tests; Claude explains how the API works
and how to keep secrets out of Git.

---

## Phase 5 — Pipeline and automation
**Goal:** one command runs everything, and GitHub runs it every day.

What it involves:
- `main.py`: connect Extract, Load, Analyse and Summarise, with logging
- GitHub Actions: run `pytest` on every push
- A scheduled daily run, after the ECB publishes its rates (around 16:00 CET on working days)
- The API key stored as a GitHub secret
- Decide how the rate history survives between runs, since GitHub Actions runners are temporary and
  `currencylens.db` is ignored by Git
- Update the README with run instructions and the project status

**Done when:** the tests run on every push, the daily job runs without manual action, and the
summary can be read somewhere (the job output or a saved file).

**Who writes what:** I write `main.py` and the workflow file; Claude explains how GitHub Actions
works, since this is new ground for me.

---

## Phase 6 (optional) — Extras
**Goal:** polish and extensions, only after everything else works.

What it involves:
- A small Streamlit dashboard
- A second data source for currencies Frankfurter doesn't cover (for example AOA, the Angolan
  kwanza)
- A formatter and linter (Ruff or Black) in the project and in the workflow

---

## Visual phase summary

| Phase | Name | Main focus |
|---|---|---|
| 0 | Setup | Environment, repository, scaffold, config |
| 1 | Extract | API calls, error handling, mocked tests |
| 2 | Load | SQLite, schema design, no duplicates |
| 3 | Analyse | Pandas, trends, cross rates |
| 4 | Summarise | AI call, secrets, prompts |
| 5 | Pipeline and automation | `main.py`, GitHub Actions, daily run |
| 6 | Extras (optional) | Dashboard, second source, linting |
