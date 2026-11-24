# OmniEngine AI — real local application

For presentation-day use on a Windows laptop. No hosting or demo answers. Python 3.11+ and internet are required. The frontend is plain HTML/CSS/JS; no Node installation is needed. FastAPI runs on localhost. This implementation uses live DuckDuckGo HTML search, not Chrome/Playwright, and parallel calls rather than the sequential flow in the original presentation.

## Run
1. Extract the ZIP. Install Python from https://www.python.org/downloads/ if necessary.
2. Double-click START_WINDOWS.bat. It creates a virtual environment, installs dependencies and opens `.env` in Notepad.
3. Fill in the API keys you own, save and close Notepad. You need at least TWO working AI providers for consensus. One works for individual answers. Blank providers are disabled. A ChatGPT subscription does not include API credits. Billing and quotas are provider-specific.
4. Open http://127.0.0.1:5000. Create a local account (no email is sent), choose providers, enter a query, and click Run engines. Keep the terminal open. Ctrl+C stops the server. For subsequent runs, you can use `.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 5000` in the extracted folder.

## Keys
- Gemini: https://aistudio.google.com/apikey
- OpenAI: https://platform.openai.com/api-keys
- Claude: https://console.anthropic.com/
- Grok: https://console.x.ai/
- Perplexity: https://www.perplexity.ai/settings/api

Use restricted keys and spending limits if available. Model names can be changed in `.env`; access varies. Do not upload `.env` or local.sqlite3 to GitHub. Each selected engine may incur charges, plus an extra synthesis call in consensus mode. Web search may be blocked or rate-limited; the app reports that honestly. A fallback link is not a successful search. The app is for localhost only, not public deployment. Prompts leave your computer for selected providers; there is no incognito/anonymous guarantee. Local passwords are salted and PBKDF2-hashed, sessions are opaque 24-hour tokens with HttpOnly/SameSite cookies. The app does not retain queries in its database; selected providers may retain data under their terms. Exported PPT files contain your answers. To clean up after the presentation, stop the server, delete local.sqlite3 and .env if desired, and revoke keys in provider consoles if no longer needed.

## Presentation-day checklist
- Test at least two providers before class. Check available credits and Wi-Fi.
- Use a short prompt, e.g. "Explain AVL tree rotations with an example."
- Compare responses in Parallel Grid; then run Super Consensus. Show the measured per-engine response times and status messages.
- Download the included project PPT or generate a result PPT from actual responses.
- If a provider fails, show its actual error; never claim a failure is a live success.

## API docs
https://ai.google.dev/gemini-api/docs
https://developers.openai.com/api/reference/chat-completions/overview
https://platform.claude.com/docs/en/api/messages
https://docs.x.ai/developers/rest-api-reference/inference/chat-completions
https://docs.perplexity.ai/

Tests use mocked HTTP only to validate the software. They do not verify live credentials or guarantee provider availability. No mocks are used by the running application.
