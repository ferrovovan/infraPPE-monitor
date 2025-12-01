#!/bin/bash


# Определяем команду python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Ошибка: Python не найден"
    exit 1
fi

# 1. Активация виртуального окружения
# Путь к скрипту активации (activate)
VENV_PATH="./venv"

if [ -f "$VENV_PATH/bin/activate" ]; then
    echo "Активируем виртуальное окружение..."
    source "$VENV_PATH/bin/activate"
else
    echo "Ошибка: Виртуальное окружение не найдено в $VENV_PATH"
    echo "Пожалуйста, создайте его командой 'python -m venv venv' и установите зависимости."
    exit 1
fi

# 2. Запуск приложения Python
echo "Запускаем приложение..."

# Мы запускаем модуль 'source.web.app'
export PYTHONPATH=$PYTHONPATH:.
streamlit run source/web/app.py

# Примечание: окружение остается активным только в рамках выполнения этого скрипта.

