@echo off
chcp 65001 >nul

echo 1. Активация виртуального окружения...
set VENV_PATH=venv

if exist "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
) else (
    echo Ошибка: Виртуальное окружение не найдено в %VENV_PATH%
    echo Пожалуйста, создайте его командой 'python -m venv venv' и установите зависимости.
    pause
    exit /b 1
)

echo 2. Запуск приложения...
set PYTHONPATH=%PYTHONPATH%;.
streamlit run source/web/app.py

pause
