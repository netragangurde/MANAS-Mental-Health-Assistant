# MANAS — AI Mental Wellness Support Assistant

MANAS is a Python and Streamlit prototype for supportive, non-clinical mental-wellness conversations. It provides separate patient and administrator workflows, therapist-style profile selection, local JSON data storage, and an LLM-powered conversational interface.

> **Safety notice:** MANAS is an educational prototype, not a medical device, diagnostic tool, or replacement for a licensed mental-health professional. Do not enter real patient records or sensitive personal health information. The sample therapist profiles are fictional demo entries and do not represent verified clinicians.

## Features

- Streamlit web interface with patient and administrator workflows
- Multi-turn conversational support using the Gemini API (configured through an OpenAI-compatible client)
- Therapist-style profile selection to personalize conversation tone
- JSON-based local storage for demo user, admin, and profile records
- Optional email notification settings
- Configurable LLM provider through environment variables

## Technology stack

- Python
- Streamlit
- Google Gemini API
- OpenAI Python SDK used as a compatible client for Gemini's OpenAI-compatible endpoint
- `python-dotenv`, NumPy, Pillow
- JSON for local prototype data

## Project files

```text
.
├── app.py
├── patient.py
├── admin.py
├── therapists.example.json   # safe, fictional demo profiles
├── data.example.json         # empty starter structure; copy to data.json locally
├── requirements.txt
├── .env.example               # placeholders only; never put real keys here
├── .gitignore
└── README.md
```

## Run locally (Windows PowerShell)

1. Install Python 3.11+ and Git.
2. Clone/download the repository and open its folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Create your local environment file and starter data files:

   ```powershell
   Copy-Item .env.example .env
   Copy-Item data.example.json data.json
   Copy-Item therapists.example.json therapists.json
   ```

6. Open `.env` and set `LLM_PROVIDER=gemini`, a valid `GEMINI_API_KEY`, and a model available to your Google AI Studio project. Do not commit `.env` or share screenshots containing secrets.
7. Start the app:

   ```powershell
   streamlit run app.py
   ```

8. Open the local URL printed by Streamlit. Use only fictional demo information while testing.

## Environment variables

See `.env.example`. Gemini is the intended provider for the current demo. API access and rate limits depend on the selected model and Google AI Studio project. OpenAI can be configured as an alternative if a valid key and API quota are available, but the legacy assessment paths should be tested against the chosen provider before relying on them.

Email notifications are optional and require valid SMTP/Gmail App Password configuration. Keep all email credentials private. If email is not configured, do not use features that require email alerts until the code handles missing settings cleanly.

## Data and privacy

- `data.json` is ignored by Git because it may contain account details and user records. Start from `data.example.json` for a fresh demo.
- `therapists.json` is kept local and ignored by Git. The public repository uses `therapists.example.json` with explicitly fictional demo profiles; verify any real-world profile source and permissions before replacing the examples.
- `.env` is ignored. `.env.example` must contain placeholders only.
- Never commit API keys, email app passwords, actual user profiles, conversation histories, or health information.

## Current limitations

- This is a prototype; it has not been security-reviewed or clinically validated.
- The original local JSON authentication/storage implementation requires hardening before any real use (including password hashing, input validation, and access-control review).
- Provider support and the older assessment/notification paths must be tested end-to-end for the selected LLM configuration.
- No clinical efficacy or diagnostic accuracy is claimed.

## Validation checklist

Before describing this project as complete, test at least:

- Patient sign-up/login and dashboard
- Admin sign-up/login and dashboard
- Therapist profile selection
- Multi-turn chat and context retention
- Behavior when the LLM key is missing, invalid, quota-limited, or times out
- Email path when configured, and graceful behavior when it is not
- Fresh installation using only the tracked files and the example templates

## License

Add a license only after confirming you have the rights to publish all code, images, and other assets in this repository.
