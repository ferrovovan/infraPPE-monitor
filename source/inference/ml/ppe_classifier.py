# ppe_classifier.py
import numpy as np
from ultralytics.engine.results import Results
from ..bbox_types import dBBox
from .models_loader import load_ppe_detect_model


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

	model = load_ppe_detect_model()
	results = model.predict(
		source=crop,
		verbose=True,
		conf=0.50  # уверенность предсказания
	)
	preds: Results = results[0]  # Для 1-ого и единственного кадра

	ppe_list: list[dBBox] = []
	for box in preds.boxes:
		xyxy = box.xyxy[0].cpu().numpy()
		x1, y1, x2, y2 = map(int, xyxy)
		
		conf_value = float(box.conf[0])
		class_value = int(box.cls[0])
		label: str = preds.names[class_value]
		print(f"label = {label}")

		ppe_bbox: dBBox = {
			"x1": max(0, min(x1, w - 1)),
			"y1": max(0, min(y1, h - 1)),
			"x2": max(0, min(x2, w - 1)),
			"y2": max(0, min(y2, h - 1)),
			"conf": conf_value,
			"label": label
		}
		ppe_list.append(ppe_bbox)

	return ppe_list
