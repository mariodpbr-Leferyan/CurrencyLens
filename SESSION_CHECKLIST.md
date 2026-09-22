# Session Checklist

A short routine to run at the start and end of every working session on CurrencyLens.

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
