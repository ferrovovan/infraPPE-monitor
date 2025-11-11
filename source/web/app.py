import streamlit as st

import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
root_path = Path(__file__).resolve().parents[2]
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from source.data.load_video import frame_generator
from source.inference.ppe_detector import detect_ppe

st.title("PPE Monitor — Prototype")

video = st.file_uploader("Загрузите видео", type=["mp4", "avi"])
if video:
    st.video(video)
    results = []

    for frame_id, frame in frame_generator(video.name):
        res = detect_ppe(frame_id, frame)
        results.append(res)
        if frame_id % 10 == 0:
            st.write(f"Кадр {frame_id}: {res['ppe_detected']}")

    st.success("Обработка завершена!")

