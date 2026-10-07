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

**What was done so far this session:**
-

---

## Template for future sessions

Copy this block for each new session:

```
## Session N — <date>

**Started at:** <time> (or **Resumed at:** <time> — **Pause since last session:** <duration>, if
opening a new session block for a session that continues later)

**What was done so far this session:**
-

**Pause flagged at <time> (<reason>)** — resumed at <time>. **Pause duration: <duration>.**

**What was done after resuming (<time> → <time or "session end">):**
-

**Session end: <time>. Total time: <duration>.**

**Status at end of session:**

**Reminders for next session:**
-
```
