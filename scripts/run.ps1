[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$VENV_PATH = Join-Path $PSScriptRoot "..\venv"
$activate = Join-Path $VENV_PATH "Scripts\Activate.ps1"

if (Test-Path $activate) {
    Write-Host "Активируем виртуальное окружение..."
    & $activate
} else {
    Write-Host "Ошибка: venv не найден по пути: $VENV_PATH"
    Write-Host "Создайте: python -m venv venv  (в корне проекта) и установите зависимости."
    exit 1
}

Write-Host "Запускаем приложение..."
$env:PYTHONPATH = "$env:PYTHONPATH;."
streamlit run ../source/web/app.py
