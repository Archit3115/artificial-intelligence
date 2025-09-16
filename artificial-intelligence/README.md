
# Artificial Intelligence

This folder will contain AI experiments, notebooks, and models.

Suggested subfolders:

Contents
- `src/` — minimal Python starter code and example generator.
- `docs/` — architecture diagrams (Mermaid) and rendered artifacts.
- `scripts/` — helper scripts for setting up Python/venv and installing git hooks.
- `.githooks/` — local git hook scripts (install via the installer in `scripts/`).

Quickstart (Windows PowerShell)

1. Install Python 3.13 (installer script provided):

```powershell
.
\scripts\setup_python_and_venv.ps1
```

2. Activate the venv and run the starter:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.
ai-dev\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.main
```

Working with docs and diagrams
- Mermaid diagrams live in `docs/` as Markdown files containing Mermaid code blocks.
- A GitHub Actions workflow (`.github/workflows/render-mermaid.yml`) can render Mermaid diagrams to `docs/diagrams/`.

Git hooks
- To enable the repo-local hooks, run the installer script:

```powershell
.
scripts\install-git-hooks.ps1
```

Contributing
- Create a branch from `main`, make changes, and open a PR targeting `main`.
- Follow the existing style used in `docs/` for Mermaid blocks (single fenced code block per diagram).

Authoring notes
- If your editor shows edited content but `git` shows an empty file, confirm the file is saved at the repo path `docs/livekit-architecture.md` and run:

```powershell
git update-index --no-assume-unchanged docs\livekit-architecture.md
git add docs\livekit-architecture.md
git commit -m "docs: restore livekit-architecture.md"
git push origin dev-101
```

License
- This repo does not include a license file. Add one if you plan to open-source it.

---

Small, focused repo to capture ideas and diagrams for experiments. Open a PR for improvements.
