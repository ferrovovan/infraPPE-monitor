$VENV_PATH = ".\venv"
$activate  = Join-Path $VENV_PATH "Scripts\Activate.ps1"

if (Test-Path $activate) {
    Write-Host "Активируем виртуальное окружение..."
    & $activate
} else {
    Write-Host "Ошибка: Виртуальное окружение не найдено в $VENV_PATH"
    Write-Host "Создайте его: python -m venv venv  и установите зависимости."
    exit 1
}

Write-Host "Запускаем приложение..."
$env:PYTHONPATH = "$($env:PYTHONPATH);."

streamlit run source/web/app.py
