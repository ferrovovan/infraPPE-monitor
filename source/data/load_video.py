# load_video.py

import cv2
from source.data.simulate_ir import rgb_to_ir


def _base_video_generator(video_path: str):
    """
    Генератор кадров с индексом.
    Возвращает пары (номер кадра, изображение np.ndarray)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Не удалось открыть видео: {video_path}")

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield idx, frame
        idx += 1
    cap.release()


def frame_generator(video_path: str):
    """
    Публичный генератор стандартных (BGR/RGB) кадров.
    """
    yield from _base_video_generator(video_path)


def ir_frame_generator(video_path: str):
    """
    Публичный генератор ИК-кадров. Применяет трансформацию.
    """
    for idx, frame in _base_video_generator(video_path):
        ir_frame = rgb_to_ir(frame)
        yield idx, ir_frame
