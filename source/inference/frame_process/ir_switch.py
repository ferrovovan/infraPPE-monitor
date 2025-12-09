import numpy as np
import cv2


def switch_to_normal(ir_image_16bit: np.ndarray) -> np.ndarray:
	"""
	Переводит одноканальный ИК-кадр (12/16 бит) в псевдо-RGB (3 канала, 8 бит).
	Это преобразование использует стандартные цветовые карты (colormap) OpenCV
	  и не является машинным обучением.
	Для обычных моделей YOLO
	
	Args:
		frame (np.ndarray): Входной ИК-кадр (numpy array, 1 канал, dtype=uint16).

	Returns:
		np.ndarray: Псевдо-цветной кадр (numpy array, 3 канала, dtype=uint8)
	"""
	# Нормализуем диапазон значений из 12/16 бит (0-4095 или 0-65535) 
	# к стандартному 8-битному диапазону (0-255).
	# cv2.NORM_MINMAX автоматически масштабирует текущий диапазон.
	ir_image_8bit = cv2.normalize(ir_image_16bit, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

	# 2. Применение цветовой карты (псевдораскрашивание)
	# COLORMAP_JET - популярная палитра для тепловых изображений (от синего к красному/горячему).
	ir_colorized_bgr = cv2.applyColorMap(ir_image_8bit, cv2.COLORMAP_JET)

	# 3. конвертация в формат для моделей YOLO.
	ir_colorized_rgb = cv2.cvtColor(ir_colorized_bgr, cv2.COLOR_BGR2RGB)

	return ir_colorized_rgb
