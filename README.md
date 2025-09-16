# artificial-intelligence

Purpose
-------
This repository collects small AI experiments, reference code, and architecture documents focused on realtime voice integration (LiveKit, WebRTC) and voice model flows (ElevenLabs). It's intended as a lightweight playground and documentation hub you can fork, extend, and use to prototype integrations quickly.

What's in this repo
-------------------
- `src/` — minimal Python starter CLI and example code. Use it as the base for experiment scripts.
- `docs/` — Markdown architecture docs (Mermaid.js diagrams) and any rendered artifacts.
- `scripts/` — helper scripts for environment setup (PowerShell helpers to install Python + venv and to install repo-local git hooks).
- `.githooks/` — local git hook scripts (install locally with the installer script in `scripts/`).
- `requirements.txt` — Python dependencies for the starter and small utilities.

Architecture documents included
------------------------------
- `docs/livekit-architecture.md` — LiveKit + ElevenLabs voice flow and component responsibilities.
- `docs/webrtc-architecture.md` — WebRTC session-level overview, signaling and ICE responsibilities.
- `docs/elevenlabs-v3-architecture.md` — ElevenLabs TTS/embedding flow, API considerations and example sequences.

Quick start (Windows PowerShell)
--------------------------------
1. Run the setup script to install Python and create a `ai-dev` virtual environment (PowerShell will request permission):

```powershell
.
scripts\setup_python_and_venv.ps1
```

2. Activate the venv and install the Python requirements:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.
ai-dev\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

3. Run the starter example:

```powershell
python -m src.main
```

Working with diagrams
---------------------
- Diagrams are stored as Mermaid blocks inside `docs/*.md`.
- CI: a GitHub Actions workflow can render these to `docs/diagrams/` (see `.github/workflows/render-mermaid.yml`).
- If GitHub shows a blank file for a doc you edited locally, ensure you saved the file to the repo path and committed it:

```powershell
git update-index --no-assume-unchanged docs\livekit-architecture.md
git add docs\livekit-architecture.md
git commit -m "docs: restore livekit-architecture.md"
git push origin dev-101
```

Contributing
------------
- Create a branch from `main` or `dev-101` for your changes. Open a PR back to `main` when ready.
- We try to keep architecture docs simple (one Mermaid fenced block per file) so GitHub's renderer and the CI renderer behave consistently.

Contact
-------
- Maintainer: Archit Srivastasva <architsrivastava3115@gmail.com>

License
-------
- No license file in this repo. Add `LICENSE` if you intend to make this code public under a formal license.

--

Short and practical — use the `docs/` files as architecture references and the `src/` starter to prototype quickly.
