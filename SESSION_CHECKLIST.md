# Session Checklist

A short routine to run at the start and end of every working session on CurrencyLens.

## First-time setup (before Session 1)

Do this once, before writing any code.

### Prerequisites

Before writing a single line of code, make sure you have:

- Python 3.11+ installed (`python3 --version` in your terminal)
- Git installed (`git --version`)
- A code editor (VS Code, since it's already in your CV skills)
- A GitHub account (you have one — `mariodpbr-Leferyan`)
- An Anthropic or OpenAI API key (for the AI summary step later — not needed yet)
- A folder where you keep your projects (e.g., `~/Projects/`)

If any of these are missing, sort it out first before moving on.

### Create the local project

This is the first real task (not busywork):

1. Open a terminal, go to wherever you keep projects, and create a folder called `CurrencyLens`.
2. Move the three project docs (`README.md`, `PROGRESS.md`, `SESSION_CHECKLIST.md`) into it.
3. Run `git init` inside it.
4. Create a Python virtual environment (`python3 -m venv venv`) and activate it.
5. Make your first commit: something like `git commit -m "Initial project structure"`.

**Why this matters:** `git init` starts tracking every change from here on — that history is itself
something you can point to (the commit log shows real, incremental work, not one giant dump). The
virtual environment keeps this project's Python packages isolated from everything else on your
machine, so dependencies don't clash between projects.

After trying it, be ready to report:

- What errors (if any) you hit
- What `git status` shows after your first commit

## Start of session

1. `cd` into the project folder.
2. `git status` — check nothing is uncommitted from last time, and that you're on the right branch.
3. `git pull` — if you ever work from more than one machine, or after using GitHub's web editor.
4. Activate the virtual environment (`source venv/bin/activate` on macOS/Linux, or
   `venv\Scripts\activate` on Windows).
5. Open `PROGRESS.md` and re-read the "Next session" notes from last time, so you remember where you
   left off.
6. Open a new session block in `PROGRESS.md` (copy the template at the bottom of the file) and fill in
   the date.

## End of session

1. Run the test suite (`pytest`) — make sure you're not leaving broken code behind.
2. `git add` and `git commit` your changes, with a clear commit message describing what changed.
3. `git push` to GitHub, so the work is backed up remotely (not just on your machine).
4. Fill in the rest of today's block in `PROGRESS.md`: what you did, what you learned, any blockers,
   and what to do next session.
5. If you changed anything sensitive (API keys, `.env`), double-check it's in `.gitignore` and was
   **not** committed. Run `git log -p -- .env` if unsure — it should return nothing.

That's it. Two minutes at each end, and future-you will always know where things stand.
