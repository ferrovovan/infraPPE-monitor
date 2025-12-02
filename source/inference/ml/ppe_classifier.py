# ppe_classifier.py
import numpy as np
from ..bbox_types import dBBox, Worker
from ultralytics import YOLO


# Грузим модель один раз (оптимально)
def load_yolo_model():
	model_path = "yolov8n.pt"
	yolo_model = YOLO(model_path)
	return yolo_model


def detect_ppe_on_worker(crop: np.ndarray) -> list[dBBox]:
	"""
	Возвращает список элементов PPE на человеке.
	bbox: локальные координаты внутри crop (слева-справа, сверху-снизу).
	Возвращает список словарей dBBox.
	"""
	if crop is None or crop.size == 0:
		# Обработка пустого входного изображения (если заглушка detect_workers вернула пустой np.ndarray)
		return []
	
	h, w = crop.shape[:2]
	
	model = load_yolo_model()
	results = model.predict(
		source=crop,
		verbose=False,
		conf=0.25  # можешь регулировать
	)
	preds = results[0]
	out: list[dBBox] = []

	# Создаем фиктивный bbox для каски, используя тип dBBox
	# Конвертируем относительные координаты в нужный формат словаря

	for box in preds.boxes:
		xyxy = box.xyxy[0].cpu().numpy()
		x1, y1, x2, y2 = map(int, xyxy)

		conf = float(box.conf[0].cpu().numpy())
		cls_id = int(box.cls[0].cpu().numpy())
		label = preds.names[cls_id]

		bbox: dBBox = {
			"x1": max(0, min(x1, w - 1)),
			"y1": max(0, min(y1, h - 1)),
			"x2": max(0, min(x2, w - 1)),
			"y2": max(0, min(y2, h - 1)),
			"conf": conf,
			"label": label
		}

		out.append(bbox)

	return out

