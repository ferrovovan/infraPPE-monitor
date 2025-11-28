# inference_source.py

# Источник внешних функций, как
#  обработка каждого кадра, взятие кадра.
# То есть механизмы _вне_ Steamlit.

from source.data.load_video import frame_generator as _frame_generator
from source.inference.ppe_detector import detect_ppe as _detect_ppe

def generate_frames(video_path: str):
    for frame_id, frame in _frame_generator(video_path):
        yield frame_id, frame

def run_inference(frame_id: int, frame):
    return _detect_ppe(frame_id, frame)

