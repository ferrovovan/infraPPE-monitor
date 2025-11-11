# source/data/load_video.py
import cv2

def frame_generator(video_path):
    """
    Генератор кадров с индексом.
    Возвращает пары (номер кадра, изображение np.ndarray)
    """
    cap = cv2.VideoCapture(video_path)
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield idx, frame
        idx += 1
    cap.release()

