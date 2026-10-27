# ScopeCraft — Proposal & Scope-of-Work Drafting Assistant

A professional Streamlit app for turning discovery notes and a selected service package into an editable proposal draft.

## Features
- Professional dark-navy sidebar and clean workspace layout
- Sidebar navigation for Overview, Client & Discovery, Scope & Deliverables, Timeline & Pricing, Template & Review, and Generated Proposal
- Session-persistent fields while navigating between sections
- Structured proposal sections: discovery, goals, scope, deliverables, assumptions, exclusions, milestones, pricing notes, client questions, and next steps
- Uses an approved company template when supplied
- Never invents pricing; missing details are flagged for confirmation
- Editable generated draft with Markdown and plain-text downloads
- Progress indicator and readiness checklist

## Run in VS Code on Windows PowerShell
Open the project folder in VS Code, then select **Terminal → New Terminal**. Make sure the terminal profile is **PowerShell**, not Bash.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `py` is not recognized, try `python --version` and use `python -m venv .venv` instead.

## Run in Bash / WSL
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Before submission
1. Test navigation and confirm fields remain filled when changing sections.
2. Generate a draft with complete information and with some fields left blank.
3. Confirm missing pricing is not invented and flagged for approval.
4. Test the Markdown and text download buttons.
5. Replace placeholders with approved company wording.
6. Publish to your GitHub account and deploy if required; submit only actual working links.
