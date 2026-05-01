@echo off
echo.
echo  ============================================
echo   Corporate Training Agent - Starting...
echo  ============================================
echo.

cd /d "%~dp0"

REM Check if venv exists, create if not
if not exist ".venv" (
    echo  [1/3] Creating virtual environment...
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Install dependencies
echo  [2/3] Installing dependencies...
pip install -q -r requirements.txt

REM Create outputs folder
if not exist "outputs" mkdir outputs

echo  [3/3] Launching server at http://localhost:8000
echo.
echo  Open your browser: http://localhost:8000
echo  Press Ctrl+C to stop.
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause
