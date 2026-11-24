@echo off
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (set "PY=python") else (set "PY=py -3")
if not exist .venv\Scripts\python.exe %PY% -m venv .venv
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail
if not exist .env copy .env.example .env >nul
 echo Edit .env with your real API keys before starting.
 echo Save and close Notepad when ready.
notepad .env
 echo Open http://127.0.0.1:5000 in your browser.
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 5000
pause
exit /b
:fail
echo Setup failed. Install Python 3.11 or newer and check your Internet connection.
pause
