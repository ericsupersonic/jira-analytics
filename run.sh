#!/bin/bash

echo "========================================"
echo "JIRA Analyzer"
echo "========================================"
echo ""

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 не установлен!"
    echo "Установите Python3: sudo apt-get install python3"
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "[INFO] Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
echo "[INFO] Установка зависимостей..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Проверка конфигурации
if [ ! -f "config.yaml" ] && [ ! -f "config.ini" ]; then
    echo "[WARNING] Файл конфигурации не найден!"
    echo "Создайте config.yaml или config.ini"
    exit 1
fi

if [ -f "config.yaml" ]; then
    echo "[INFO] Используется config.yaml"
elif [ -f "config.ini" ]; then
    echo "[INFO] Используется config.ini"
fi

# Запуск программы
echo ""
echo "[INFO] Запуск анализатора..."
echo ""
python3 main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCESS] Анализ завершен успешно!"
    echo "Результаты сохранены в директории output/"
else
    echo ""
    echo "[ERROR] Произошла ошибка при выполнении!"
    exit 1
fi