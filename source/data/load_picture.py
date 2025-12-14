# load_picture.py

import cv2
from .simulate_ir import rgb_to_ir


def _base_picture_taker(picture_path: str):
	"""
	Базовый открыватель изображений
	Возвращает изображение np.ndarray в RGB
	"""
	img_bgr = cv2.imread(picture_path, cv2.IMREAD_COLOR)
	if img_bgr is not None:
		print("Изображение успешно загружено. Размеры:", img_bgr.shape)
	else:
		raise ValueError(f"Не удалось загрузить изображение: {picture_path}")
	
	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	return img_rgb


def picture_taker(picture_path: str):
	"""
	Публичный открыватель изображений.
	"""
	return _base_picture_taker(picture_path)


def ir_picture_taker(picture_path: str):
	"""
	Публичный открыватель симуляции ИК-изображений. Применяет трансформацию.
	"""
	frame = _base_picture_taker(picture_path)
	return rgb_to_ir(frame)
