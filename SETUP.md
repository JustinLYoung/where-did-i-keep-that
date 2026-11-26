# Development Setup

Install Python 3.11 or newer. Open a terminal in the project repository folder (the folder containing `requirements.txt`).

## macOS / Ubuntu

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Windows 10 (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

That's it. Run the commands for your operating system once after cloning the repository. Run the install command again whenever `requirements.txt` changes.

## Environment Variables

Copy `.env.example` to a new file named `.env` in the project folder and fill in both values:

- `GEMINI_API_KEY`: your Gemini API key from Google AI Studio
- `SECRET_KEY`: a random string used to keep login sessions secure. Generate one with:

```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

The app will not start without `SECRET_KEY`.