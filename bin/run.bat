@echo off
chcp 65001 >nul
echo ========================================
echo JIRA Analyzer
echo ========================================
echo.

REM Переходим в корень проекта
cd /d "%~dp0\.."

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Check configuration
if not exist "config\config.yaml" if not exist "config.yaml" (
    echo [WARNING] Configuration file not found!
    echo Create config\config.yaml or config.yaml
    pause
    exit /b 1
)

if exist "config\config.yaml" (
    echo [INFO] Using config\config.yaml
) else if exist "config.yaml" (
    echo [INFO] Using config.yaml
)

REM Run the analyzer
echo.
echo [INFO] Starting analyzer...
echo.
python main.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred during execution!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Analysis completed successfully!
echo Results saved to output/ directory
echo.
pause