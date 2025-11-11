
Pipeline:
[data/load_video.py] → [inference/ppe_detector.py] → [web/app.py]

Transport: кадры (numpy.ndarray), результаты (dict)
Формат передачи данных:
• Результаты инференса: dict -> JSON
• Идентификатор кадра: frame_id:int

