# Repository Guidelines

## Project Structure & Module Organization
`main.py` is the entry point that starts the PyQt6 app and system tray. Core
logic lives in `src/` (windows, managers, state, input monitor). Content data is
stored in `src/data/*.json`. UI images are in `assets/`. Runtime state and logs
are written to `save_data.json` and `logs/app.log`. The root `memory.md` and
`plan.md` are working notes.

## Build, Test, and Development Commands
- `python -m pip install -r requirements.txt` installs dependencies.
- `python main.py` runs the desktop app.
There is no separate build step.

## Coding Style & Naming Conventions
Use 4-space indentation and keep imports grouped (stdlib, third-party, local).
Prefer `snake_case` for modules/functions and `PascalCase` for classes. Qt window
modules follow `*_window.py` with classes named `*Window`.

## Testing Guidelines
There is no automated test suite in this repo. Validate changes by running the
app and checking window behavior, tray icon actions, and `logs/app.log`. If you
add tests, place them under `tests/` and document the runner in this file.

## Runtime Data & Assets
Treat `save_data.json` as user state; preserve the schema and add migrations if
you change keys. Keep `src/data/*.json` and `assets/` filenames stable because
UI code loads them by name.

## Commit & Pull Request Guidelines
Git history uses short, descriptive commit messages (often concise Chinese
phrases). Keep messages brief and action-focused. PRs should include a summary,
testing notes (commands run), and screenshots/GIFs for UI changes; link related
issues when applicable.
