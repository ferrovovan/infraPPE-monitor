import cv2
from source.data.simulate_ir import rgb_to_ir


def frame_generator(video_path):
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
        yield idx, rgb_to_ir(frame)
        idx += 1
    cap.release()
