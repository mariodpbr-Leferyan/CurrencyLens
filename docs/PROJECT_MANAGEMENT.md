# Project Management — GitHub Projects

This document explains how CurrencyLens is managed with GitHub Projects (Scrum/Kanban), and contains
the backlog organised by Epic and Sprint. It follows the same setup as HomeBase, scaled down to a
smaller project.

## Why GitHub Projects

GitHub Projects already supports:
- A Kanban board (Backlog / To Do / In Progress / In Review / Done)
- Custom fields (Epic, Sprint, Priority)
- Direct links to Issues and Pull Requests in the repository, so the board and the code live in the
  same place
- Different views of the same data (Board, Table, Roadmap)

The commit history linked to concrete tasks is exactly what I want to be able to show in a
portfolio.

---

## Part 1 — Initial setup (done once)

### 1.1. Create the Project

1. In the `CurrencyLens` repository on GitHub, open the **Projects** tab.
2. Click **New project** and choose the **Board** template.
3. Name it `CurrencyLens Roadmap`.

### 1.2. Create custom fields

Inside the Project, click the **+** next to the column headers (or "..." → *Settings* → *Fields*):

| Field | Type | Values |
|---|---|---|
| **Status** | Single select (default) | Backlog, To Do, In Progress, In Review, Done |
| **Epic** | Single select | Epic 1 – Foundation, Epic 2 – Extract, Epic 3 – Load, Epic 4 – Analyse, Epic 5 – Summarise, Epic 6 – Test & Automate, Epic 7 – Extras |
| **Sprint** | Single select | Sprint 0, Sprint 1, Sprint 2, Sprint 3, Sprint 4, Sprint 5 (dates in Part 3) |
| **Priority** | Single select | Must-have, Nice-to-have |

### 1.3. Create labels in the repository

Under **Issues → Labels → New label**, create one label per Epic (`epic-1-foundation`,
`epic-2-extract`, `epic-3-load`, `epic-4-analyse`, `epic-5-summarise`, `epic-6-test-automate`,
`epic-7-extras`) and one per phase (`phase-0` to `phase-6`).

### 1.4. Create views

Inside the Project, use **+ New view** to create at least two views:
- **Board by Sprint** — Kanban view grouped by `Status`, filtered by the current `Sprint`. This is the
  one used day to day.
- **Table by Epic** — table view grouped by `Epic`, to see the overall progress.

---

## Part 2 — How to create and use an Issue (task)

Each line in the backlog below (Part 3) becomes an **Issue** on GitHub:

1. **Issues → New issue**
2. A short, clear title (for example "Write fetch_rates.py: request the latest rates")
3. A description of what needs to be done, with a checklist when it helps
4. Add the Epic and Phase labels
5. In the right sidebar, under **Projects**, add it to `CurrencyLens Roadmap`
6. Inside the Project, set the `Epic`, `Sprint` and `Priority` fields, and `Status = Backlog`

When starting a task: `Status = In Progress`. Once the code is written and tested: `In Review` (even
working alone, reviewing before closing is a good habit). Once committed and pushed: `Done`.

Tip: when opening an Issue, the **Create a branch** button links a new branch to that Issue
automatically.

At the end of every session, the board gets updated: finished issues move to Done, and the next task
moves to In Progress.

---

## Part 3 — Backlog (tasks by Sprint)

Only the current sprint and the next one get Issues, so managing tasks never takes more time than
writing code. Sprints last one week.

### Sprint 0 — Setup (Sep 22 – Oct 6) · Epic 1 · done
- [x] Install Python and Git, confirm versions
- [x] Create the `CurrencyLens` repository on GitHub
- [x] Create the virtual environment (`venv`) and activate it
- [x] Create `.gitignore`
- [x] Install `requests` and generate `requirements.txt`
- [x] First commit and push
- [x] Scaffold the package (`currencylens/`) and `tests/`
- [x] Write `config.py`

### Sprint 1 — Docs and Extract (Oct 7 – 13) · Epic 1 and Epic 2
- [ ] Create the `docs/` folder with `ROADMAP.md` and `PROJECT_MANAGEMENT.md` · Epic 1
- [ ] Set up the GitHub Projects board (fields, labels, views) · Epic 1
- [ ] Fix the outdated Frankfurter link in `README.md` · Epic 1
- [ ] Write `fetch_rates.py`: request the latest rates · Epic 2
- [ ] Turn the API response into a clean structure · Epic 2
- [ ] Error handling: timeouts and HTTP errors · Epic 2
- [ ] Tests for `fetch_rates.py` with a mocked HTTP call · Epic 2
- [ ] Commit + update `PROGRESS.md`

### Sprint 2 — Load (Oct 14 – 20) · Epic 3
- [ ] Write `docs/DATA_MODEL.md` (table design)
- [ ] Write `docs/ARCHITECTURE.md` (pipeline and data flow)
- [ ] `database.py`: connection and table creation
- [ ] Insert rates without duplicates
- [ ] Read the history back
- [ ] Tests for `database.py` with a temporary database

### Sprint 3 — Analyse (Oct 21 – 27) · Epic 4
- [ ] Load the history into a Pandas DataFrame
- [ ] Day-over-day and week-over-week percentage changes
- [ ] Moving averages (windows from `config.py`)
- [ ] Cross rates between any two currencies
- [ ] Handle missing days and short history
- [ ] Tests for `analysis.py`

### Sprint 4 — Summarise (Oct 28 – Nov 3) · Epic 5
- [ ] Choose the AI provider and add its SDK to `requirements.txt`
- [ ] Set up `.env` and `.env.example` for the API key
- [ ] Build the prompt from the analysis results
- [ ] Call the model and handle failures
- [ ] Tests for `summarize.py` with a mocked client

### Sprint 5 — Pipeline and automation (Nov 4 – 10) · Epic 6
- [ ] `main.py`: connect the four stages, with logging
- [ ] GitHub Actions: run `pytest` on every push
- [ ] Store the API key as a GitHub secret
- [ ] Schedule the daily run
- [ ] Decide how the rate history persists between runs
- [ ] Update the README with run instructions and the project status

### Future — Extras · Epic 7
- [ ] Streamlit dashboard
- [ ] Second data source for currencies Frankfurter doesn't cover (such as AOA)
- [ ] Formatter and linter (Ruff or Black)
