import numpy as np
from ..bbox_types import dBBox, Worker
from ultralytics import YOLO


def load_yolo_model():
	model_path = "yolov8n.pt"
	yolo_model = YOLO(model_path)
	return yolo_model


def detect_workers_dummy(frame: np.ndarray) -> list[Worker]:
	# Заглушка для демонстрации структуры возвращаемых данных,
	# если модель еще не загружена
	dummy_bbox_data = {"x1": 100, "y1": 100, "x2": 200, "y2": 300, "conf": 0.9, "label": "person"}
	# Используем пустой массив numpy в качестве заглушки для crop
	dummy_crop = np.zeros((100, 100, 3), dtype=np.uint8) 

	return [
		{
			'id': 1,
			'bbox': dummy_bbox_data,
			'crop': dummy_crop,
			'ppe_rel': [],
			'ppe': []
		}
	]


def detect_workers(frame: np.ndarray) -> list[Worker]:
	"""
	Обнаруживает людей (рабочих) на кадре с использованием YOLO модели
	и возвращает структурированный список объектов Worker.
	"""

	model = load_yolo_model()

	results = model(frame)[0]   # берём результат первого изображения
	boxes = results.boxes       # ultralytics Boxes()

	workers_list: list[Worker] = []
	worker_id_counter = 1

	for box in boxes:
		cls = int(box.cls[0])                # индекс класса
		label = model.names[cls]             # строка класса
		conf = float(box.conf[0])
		# Проверяем, что класс объекта это 'person'
		if label != "person":
			continue
		# xyxy -> ints
		x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

		# Создаем словарь dBBox
		bbox_data: dBBox = {
			"x1": x1,
			"y1": y1,
			"x2": x2,
			"y2": y2,
			"conf": conf,
			"label": "worker"
		}

		# На этом этапе мы еще не знаем crop и ppe_rel/ppe, 
		# но мы создаем базовую структуру Worker
		new_worker: Worker = {
			'id': worker_id_counter,
			'bbox': bbox_data,
			'crop': np.ndarray([]),  # Заглушка, будет заполнена позже в 'cropper.py'
			'ppe_rel': [],           # Заглушка, будет заполнена позже в 'ppe_classifier.py'
			'ppe': []                # Заглушка, будет заполнена позже
		}

		workers_list.append(new_worker)
		worker_id_counter += 1

	return workers_list
