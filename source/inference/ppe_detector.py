import random

def detect_ppe(frame_id, frame):
    """
    Простая заглушка детектора.
    Возвращает результат для каждого кадра.
    """
    return {
        "frame_id": frame_id,
        "ppe_detected": random.choice([True, False]),
    }

