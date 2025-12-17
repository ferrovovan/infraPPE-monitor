# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# worker_detector.py

import numpy as np
from ..bbox_types import dBBox, Worker
from .models_loader import load_worker_detect_model


def detect_workers(frame: np.ndarray) -> list[Worker]:
	"""
	Обнаруживает людей (рабочих) на кадре с использованием YOLO модели
	и возвращает структурированный список объектов Worker.
	"""

	model = load_worker_detect_model()
	results = model.predict(
		source=frame,
		verbose=True,
		conf=0.75  # уверенность предсказания
	)
	preds = results[0]   # Для 1-ого и единственного кадра
	boxes = preds.boxes  # ultralytics Boxes()

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
