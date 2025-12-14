#!/bin/bash
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan

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

# 3. Проверка наличия линтера
if command -v flake8 &> /dev/null; then
    echo "Линтер flake8 найден. Продолжаем выполнение скрипта."
else
    echo "Ошибка: flake8 не установлен в текущем виртуальном окружении."
    echo "Пожалуйста, установите его (например, 'pip install flake8' или 'pip install .[devel]')."
    exit 1
fi

# 3. Запуск flake8
echo "Запускаем линтер flake8..."
export PYTHONPATH=$PYTHONPATH:.
flake8 source/

# Примечание: окружение остается активным только в рамках выполнения этого скрипта.
