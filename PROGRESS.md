# Progress Log — CurrencyLens

This log tracks work sessions on the project: what was done, time spent, and pauses. Entries are
added chronologically, most recent at the bottom. Time and pause data is self-reported by me at the
start/end of each session, since durations can't be tracked automatically.

**How to use this log each session:**
- At the start: state the time (and, if resuming after a break, roughly how long the pause was).
- During a pause (lunch, break, stepping away): flag the time so it can be logged.
- At the end: state the end time; a short status summary gets added of what was accomplished.

---

## Session 0 — Planning

**Date:** September 22, 2026

**What I did:**
- Decided on the project: an ETL pipeline for currency exchange rates, with an AI-generated summary
  step, unit tests, and a CI/CD pipeline — built on top of my existing EUR/USD Currency Converter
  script.
- Chose the name **CurrencyLens**.
- Planned the project structure with Claude (see README.md for the layout).
- Wrote the initial README.md and this progress log.

**Status at end of session:** Planning complete, no code written yet.

**Next session:**
- Set up the local project folder, git repository, and a Python virtual environment.
- Write `requirements.txt`.
- Start `config.py` (the list of currency pairs to track).

---

## Session 1 — September 22, 2026

**Started at:** 13:07.

**What was done:**
- Created the local `CurrencyLens` project folder and moved in the three starter docs (`README.md`,
  `PROGRESS.md`, `SESSION_CHECKLIST.md`)
- Ran `git init`, created the `CurrencyLens` repository on GitHub, linked it as `origin`
- Hit `git pull` failing with "no tracking information" — learned this is normal for a repo with no
  upstream branch set yet
- Hit `git push -u origin main` failing with "src refspec main does not match any" — traced to two
  compounding issues: the local default branch was `master` (older Git default) rather than `main`,
  and initially there were no commits yet at all, so no branch truly existed
- Fixed by renaming the branch (`git branch -M main`) and making the first commit (`git add .` /
  `git commit`) before pushing — first push to GitHub succeeded
- Created and activated a Python virtual environment (`venv`) on Windows (`python -m venv venv`,
  `venv\Scripts\activate`)
- Wrote a `.gitignore` (`venv/`, `__pycache__/`, `*.pyc`, `.env`, `.vscode/`, `.DS_Store`) to keep the
  virtual environment and future secrets out of version control
- Hit a subtle bug: the first `.gitignore` was pasted in as a single line, so the leading `#` comment
  swallowed every pattern on that line — Git kept tracking `venv/` (confirmed by `git add .` staging
  hundreds of `venv/` files). Learned that `.gitignore` has no smart parsing — line breaks between
  patterns are load-bearing, and paste operations from other sources don't always preserve them
- Fixed by retyping `.gitignore` manually (one pattern per line), verified with `git status` that
  `venv/` dropped out of the untracked list
- Committed and pushed `.gitignore` — confirmed clean `git status` with `venv/` properly ignored

**Pause flagged at 14:04 (lunch)** — resumed at 16:28. **Pause duration: 2h 24min.**

**What was done after resuming (16:28 → 17:51):**
- Installed `requests` (plus its dependencies `certifi`, `charset-normalizer`, `idna`, `urllib3`) and
  generated `requirements.txt` via `pip freeze` — committed and pushed
- Planned the project's code structure: decided on a packaged layout (`currencylens/` with an
  `__init__.py`), one module per pipeline stage (`fetch_rates.py`, `database.py`, `analysis.py`,
  `summarize.py`), plus `config.py` for settings and `main.py` to orchestrate the pipeline
- Discussed the alternative "src layout" (`src/` + `pyproject.toml`) and why it wasn't worth the
  extra packaging ceremony for a project that isn't distributed as a library — documented the
  reasoning in `README.md`
- Updated `README.md` with a **Project structure** section and a filled-in **Setup** section
- Scaffolded the actual folders and empty placeholder files (`currencylens/` and `tests/`), committed
  and pushed them
- Started planning `config.py` — paused before writing any actual content

**Session end: 17:51. Total time: ~2h 20min** (57 min before lunch + 1h 23min after, excluding the
2h 24min lunch pause).

**Status at end of session:** Local project fully set up — Git repo, GitHub remote, virtual
environment, `.gitignore`, `requirements.txt`, and the full package/tests folder scaffold, all
committed and pushed. `config.py` has an empty placeholder file but no content yet.

**Reminders for next session:**
- Before writing `config.py`, answer these three questions (asked at the end of this session):
  1. Which currency pairs do I actually want to track (base currency + target list) for the
     Frankfurter API?
  2. What's the Python naming convention for constants that don't change at runtime?
  3. Besides the currency list, what other *settings* (not logic) belong in `config.py`, based on
     what `fetch_rates.py`, `database.py`, and `summarize.py` will each need to know?

---

## Session 2 — October 6, 2026

**Resumed at:** 15:08. **Pause since last session: 13 days, 21h 17min** (Sept 22, 17:51 → Oct 6,
15:08).

**What was done:**
- Ran the start-of-session checklist: `git status` clean, `git pull` up to date. Noticed the
  virtual environment wasn't active yet and activated it
- Raised the question of a `docs/` folder and sprints/epics like in HomeBase. Decided on a lean docs
  set (`ARCHITECTURE`, `DATA_MODEL`, `ROADMAP`, `PROJECT_MANAGEMENT`) and a HomeBase-style GitHub
  Projects board (Epic, Sprint, Priority fields; Board and Table views) — both postponed to the next
  session. Shared HomeBase's `ROADMAP.md` and `PROJECT_MANAGEMENT.md` to use as templates
- Worked through the three `config.py` questions: which currencies to track (EUR as base; rates
  between other currencies can be derived from EUR-based rates instead of fetched), the constant
  naming convention (`UPPER_SNAKE_CASE`, PEP 8), and which settings belong in a config file (values
  that may change without touching logic, or that several modules need)
- Researched the data source: the BIS 2025 ranking of most traded currencies, and the Frankfurter
  docs — base URL `https://api.frankfurter.dev/v1`, parameters `base` and `symbols`, 30 supported
  currencies, rates published on working days around 16:00 CET. The Angolan kwanza (AOA) isn't
  supported, so it's left out for now; a second data source could be added later
- Wrote `currencylens/config.py`: `API_BASE_URL`, `BASE_CURRENCY`, `REQUEST_TIMEOUT_SECONDS`,
  `TARGET_CURRENCIES` (dict of code → name for the 29 supported currencies other than EUR),
  `PROJECT_ROOT` / `DB_PATH` (built with `pathlib`, so the database always lands in the project
  root), and `MOVING_AVERAGE_WINDOWS`
- Code review fixes on `config.py`: removed `DATE` (it was missing its imports, and a value computed
  at import time doesn't belong in a config file — dynamic values belong in the logic), turned the
  URL comment into a constant, removed `EUR` from the targets, PEP 8 formatting (4 spaces, closing
  brace on its own line, trailing comma), and added comments in my own voice
- Verified the file imports cleanly and `DB_PATH` points at `CurrencyLens\currencylens.db`
- Added `currencylens.db` to `.gitignore`, then committed and pushed `config.py`

**Session end: 17:13. Total time: 2h 05min.** No pauses.

**Status at end of session:** `config.py` is complete and pushed. Nothing else has code yet.

**Reminders for next session:**
- Create the `docs/` folder with the lean set (`ARCHITECTURE`, `DATA_MODEL`, `ROADMAP`,
  `PROJECT_MANAGEMENT`), using HomeBase's `ROADMAP.md` and `PROJECT_MANAGEMENT.md` as templates
  (share them again, since I don't keep them between sessions)
- Set up the GitHub Projects board: Epic, Sprint and Priority fields, labels, Board and Table views
- Fix the outdated Frankfurter link in `README.md` (the docs are at `frankfurter.dev/v1`)
- Start `fetch_rates.py` (Extract): call the `/latest` endpoint with `requests`, using the settings
  from `config.py`, including the timeout
- Write `DATA_MODEL.md` (the SQLite table design) before starting `database.py`
- When reaching the automation stage: decide how the rate history persists, since GitHub Actions
  runners are temporary and `currencylens.db` is ignored by Git
- Later: add a formatter/linter (Ruff or Black) to the project, and consider a second data source
  for currencies Frankfurter doesn't cover (such as AOA)

---

## Session 3 — October 7, 2026

**Resumed at:** 14:39. **Pause since last session: 21h 26min** (Oct 6, 17:13 → Oct 7, 14:39).

**What was done:**
- Ran the start-of-session checklist and re-read the reminders from Session 2
- Created the `docs/` folder with `ROADMAP.md` (phases 0–6, each with goal, what it involves, done
  criteria and who writes what) and `PROJECT_MANAGEMENT.md` (board setup, issue workflow, backlog by
  sprint), using HomeBase's versions as templates
- Set up the GitHub Projects board: fields (Status, Epic, Sprint, Priority), labels, and the Board and
  Table views. Learned where Epics and Sprints are created and how to set them on each issue
- Designed `fetch_rates.py` before writing it: it returns only the date plus one rate per currency.
  The "amount to compare" feature is not part of Extract — it will be computed locally later as
  `amount × rate`, in `analysis.py` or the interface
- Compared three ways to return the data (tuple, dict, frozen dataclass) with a small runnable demo,
  and chose a frozen dataclass, `RatesSnapshot(date, rates)`: named fields instead of positions, typo
  protection from the editor, and attributes that can't be reassigned
- Wrote `fetch_latest_rates()`: builds the URL and parameters from `config.py`, calls the API with
  `requests.get(..., timeout=...)`, checks the status with `raise_for_status()`, reads the JSON, and
  converts the date string with `date.fromisoformat()`. A live call returned the rates for
  2026-10-07: 29 currencies, matching `TARGET_CURRENCIES`
- Ran two failure experiments to see how the code breaks: a typo in the URL gave `HTTPError` (404,
  raised by `raise_for_status()`), and a 0.001 s timeout gave `ReadTimeout` (raised by
  `requests.get`). Learned to read a traceback from the last line upward, and that both exceptions
  inherit from `requests.exceptions.RequestException`
- Started the error handling: a custom `RatesFetchError`, a short `try/except` around the network
  call that re-raises with `raise ... from error`, and a second one that checks the response format
- Code review found three bugs that only appear when something fails — `RatesFetchError` was never
  defined, `from API_BASE_URL` should be `from error`, and `datefromisoformat` should be `ValueError`.
  The success run hid them because Python only looks up names when the line runs. Also noted PEP 8
  fixes (two blank lines between top-level definitions, no space before a call's parenthesis,
  indentation, trailing spaces, docstring layout with a `Raises:` section) and the typo "ne date"

**Session end: 18:17. Total time: 3h 38min.** No pauses.

**Status at end of session:** `fetch_latest_rates()` works for the success case. The error handling is
written but not finished: the three bugs above still need fixing, and the failure cases have to be
re-tested. Docs and the board are done. Nothing from `fetch_rates.py` is committed yet.

**Reminders for next session:**
- Fix the three bugs and the style points in `fetch_rates.py`, then re-run both failure experiments
  (URL typo and 0.001 s timeout): each must end in `RatesFetchError` with the "direct cause" line
  above it
- After the experiments, put the URL back to `/latest` and `REQUEST_TIMEOUT_SECONDS` back to `10`,
  and check with `git diff` that `config.py` is unchanged
- Delete any scratch files (`demo.py`, `try_fetch.py`) so they are not committed
- Commit and push `fetch_rates.py`; move the finished cards (write `fetch_rates.py`, clean structure,
  error handling) to Done on the board
- Fix the outdated Frankfurter link in `README.md` (`https://frankfurter.dev/`), if not done yet
- Write the tests for `fetch_rates.py` with a mocked HTTP call (first: what mocking is and why tests
  must never touch the real network)
- Check that the docs, README and `PROGRESS.md` changes from this session are on GitHub
  (`git status` and `git log --oneline -5`)
- Before starting `database.py`: write `docs/DATA_MODEL.md`
- Later: decide how the rate history persists in GitHub Actions, add Ruff or Black (a linter would
  have caught the undefined names), and consider a second data source for AOA

---

## Template for future sessions

Copy this block for each new session:

```
## Session 4 — October 19, 2026

**Resumed at:** 12:24. **Pause since last session: 11 days, 18h 07min** (Oct 7, 18:17 → Oct 19,
12:24).

**What was done so far this session:****
-

**Pause flagged at <time> (<reason>)** — resumed at <time>. **Pause duration: <duration>.**

**What was done after resuming (<time> → <time or "session end">):**
-

**Session end: <time>. Total time: <duration>.**

**Status at end of session:**

**Reminders for next session:**
-
```
