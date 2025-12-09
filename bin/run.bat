@echo off
echo ========================================
echo JIRA Analyzer
echo ========================================
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не установлен!
    echo Скачайте Python с https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Проверка виртуального окружения
if not exist "venv" (
    echo [INFO] Создание виртуального окружения...
    python -m venv venv
)

REM Активация виртуального окружения
call venv\Scripts\activate.bat

REM Установка зависимостей
echo [INFO] Установка зависимостей...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Проверка конфигурации
if not exist "config.yaml" if not exist "config.ini" (
    echo [WARNING] Файл конфигурации не найден!
    echo Создайте config.yaml или config.ini
    pause
    exit /b 1
)

if exist "config.yaml" (
    echo [INFO] Используется config.yaml
) else if exist "config.ini" (
    echo [INFO] Используется config.ini
)

REM Запуск программы
echo.
echo [INFO] Запуск анализатора...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Произошла ошибка при выполнении!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Анализ завершен успешно!
echo Результаты сохранены в директории output/
echo.
pause

