# drawer.py
import cv2
import numpy as np
from ..bbox_types import dBBox, Worker


def draw_ppe(frame: np.ndarray, workers: list[Worker]) -> np.ndarray:
	"""
	Рисует рамки PPE на кадре.
	"""
	out = frame.copy()
	for worker in workers:
		bbox = worker["bbox"]
		# 1. Подготовка координат и текста
		# OpenCV ожидает координаты в виде кортежей целых чисел (int)
		p1 = (int(bbox["x1"]), int(bbox["y1"]))
		p2 = (int(bbox["x2"]), int(bbox["y2"]))
		
		# Текст надписи: ID рабочего и, если есть, метка ("person")
		label_text = f"Worker ID: {worker['id']}"

		# 2. Рисуем рамку рабочего (синим)
		cv2.rectangle(out, p1, p2, (255, 0, 0), 2)  # Синий
		
		# 3. Рисуем надпись
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 0.6
		font_thickness = 2
		text_color = (255, 255, 255) # Белый текст
		bg_color = (255, 0, 0)       # Синий фон под текстом (опционально)

		# Рассчитываем положение текста: над верхним левым углом рамки
		# Сдвигаем на 10 пикселей вверх и 5 вправо от начала рамки
		text_pos = (p1[0] + 5, p1[1] - 10)

		# Опционально: Рисуем прямоугольник под текстом для лучшей читаемости
		(text_width, text_height), baseline = cv2.getTextSize(label_text, font, font_scale, font_thickness)
		text_bg_end = (text_pos[0] + text_width, text_pos[1] - text_height - baseline)
		cv2.rectangle(out, text_pos, text_bg_end, bg_color, -1) # Заливка фона

		# Наносим текст
		cv2.putText(out, 
			label_text, 
			text_pos, 
			font, 
			font_scale, 
			text_color, 
			font_thickness, 
			cv2.LINE_AA)

		for ppe in worker["ppe"]:
			ppe_p1 = (int(ppe["x1"]), int(ppe["y1"]))
			ppe_p2 = (int(ppe["x2"]), int(ppe["y2"]))
			# Рисуем worker["ppe"]["bbox"] зелёным
			cv2.rectangle(out, ppe_p1, ppe_p2, (0, 255, 0), 2)  # Зелёный
			
			# Опционально: надпись для PPE
			if ppe.get("label"):
				cv2.putText(out, ppe["label"], (ppe_p1[0], ppe_p1[1] - 5),
					cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1
				)
	return out
