@echo off
chcp 65001 >nul
echo ========================================
echo JIRA Analyzer - Test Suite
echo ========================================
echo.

REM Go to project root
cd /d "%~dp0\.."

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    pause
    exit /b 1
)

REM Activate venv
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -q -r requirements.txt
pip install -q -r requirements-dev.txt

REM Clean old results
echo [INFO] Cleaning old test results...
if exist "allure-results" rmdir /s /q allure-results
if exist "htmlcov" rmdir /s /q htmlcov
if exist ".pytest_cache" rmdir /s /q .pytest_cache

REM Run tests
echo.
echo [INFO] Running tests...
echo.
pytest tests/ -v --alluredir=allure-results --cov=src --cov-report=html --cov-report=term

if errorlevel 1 (
    echo.
    echo [ERROR] Some tests failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All tests passed!
echo.
echo [INFO] Coverage report: htmlcov\index.html
echo [INFO] Allure results: allure-results\
echo.
echo To view Allure report run:
echo   allure serve allure-results
echo.
pause