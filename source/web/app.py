import streamlit as st

import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
root_path = Path(__file__).resolve().parents[2]
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from source.data.load_video import frame_generator
from source.inference.ppe_detector import detect_ppe

import tempfile
import time


st.title("PPE Monitor — Prototype")

video = st.file_uploader("Загрузите видео", type=["mp4"])
if video:
    fps = st.slider("Скорость воспроизведения (кадров/сек)", 1, 30, 5)
    start_btn = st.button("▶ Запустить обработку")

    if start_btn:
        # Сохраняем видео во временный файл
        temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video_path.write(video.read())
        temp_video_path.close()

        # окошки
        frame_window = st.empty()   # область для обновления кадра
        text_window = st.empty()    # область для статуса
        progress = st.progress(0)   # полоса прогресса

        total_frames = 1000
        start_time = time.time()

        # обработка по кадрово
        for frame_id, frame in frame_generator(temp_video_path.name):
            res = detect_ppe(frame_id, frame)

            frame_window.image(frame, caption=f"Кадр {frame_id}: {res['ppe_detected']}", channels="BGR")
            text_window.text(f"Обнаружено: {res['ppe_detected']}")
            progress.progress((frame_id + 1) / total_frames)

            time.sleep(1.0 / fps)
        total_time = time.time() - start_time
        st.success("Обработка завершена за {total_time:.1f} секунд!")

