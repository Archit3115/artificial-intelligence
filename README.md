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

# Quick Start Guide: AI Agent (Jarvis)

This guide provides the steps to set up and run the local "Jarvis" AI agent on Windows using PowerShell, as specified in the project's `README.md` [1, 2].

---

## Prerequisites

- Windows with PowerShell.  
- Git installed.  
- Your ElevenLabs API key.  

---

## Step 1: Clone the Repository

If you haven't already, clone the `artificial-intelligence` repository to your local machine.

```bash
git clone https://github.com/Archit3115/artificial-intelligence.git
cd artificial-intelligence
```

---

## Step 2: Set Up Python and Virtual Environment

This project includes a helper script to install a project-local version of Python and create a virtual environment named **ai-dev**.  
Run the following command in PowerShell. You may be prompted for administrative permissions to proceed.

```powershell
. scripts\setup_python_and_venv.ps1
```

---

## Step 3: Set Your ElevenLabs API Key

The agent requires your ElevenLabs API key to generate speech. Set it as an environment variable for your current PowerShell session. Replace `"your_key_here"` with your actual key.

```powershell
$env:ELEVEN_API_KEY="your_key_here"
```

> **Note**: This variable is only set for the current terminal session. You will need to set it again if you open a new terminal.

---

## Step 4: Activate Environment and Install Dependencies

Activate the virtual environment and install the required Python packages from the `requirements.txt` file.  
The `Set-ExecutionPolicy` command may be needed to allow the activation script to run.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\ai-dev\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## Step 5: Run the Jarvis Agent

With the environment set up and dependencies installed, you can now run the agent. The main script is located in the `src/` directory, which is the designated location for the starter CLI and example code.

```powershell
python -m src.main
```

The agent will start, greet you, and begin listening for your commands through your microphone.

---

This guide is based on the instructions provided in the [Archit3115/artificial-intelligence](https://github.com/Archit3115/artificial-intelligence) repository.


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
