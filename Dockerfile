FROM python:3.11-slim

# Настройка окружения
ENV PATH="/app/venv/bin:$PATH" \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0


WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    # Добавьте эти, если планируете расширенную работу с изображениями/видео
    libsm6 \
    libxext6 \
    libxrender1
# Очистка кэша для уменьшения размера образа
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN python -m venv venv

COPY requirements.txt .
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install opencv-python numpy streamlit ultralytics
# RUN pip install --no-cache-dir -r requirements.txt


# Код приложения
COPY source ./source/
COPY models ./models/
COPY README.md .
COPY LICENSE .


# Открываем порт (8501 streamlit standart)
EXPOSE 8501

# Запускаем приложение
ENV PYTHONPATH="/app"
CMD ["streamlit", "run", "source/web/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

