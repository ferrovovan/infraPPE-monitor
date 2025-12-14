# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# ir_switch.py
import numpy as np
import cv2


def ir_to_jet(ir_image_16bit: np.ndarray) -> np.ndarray:
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


def ir_to_gray(ir_image_16bit: np.ndarray) -> np.ndarray:
	"""
	Преобразует одноканальный ИК-кадр (12/16 бит) в 3-канальное изображение в оттенках серого.
	YOLOv8 нормально работает с такими изображениями.

	Args:
	ir_image_16bit: Входной ИК-кадр (numpy array, 1 канал, dtype=uint16).

	Returns:
	np.ndarray: 3-канальное изображение в оттенках серого (dtype=uint8)
	"""
	# 1. Нормализуем 16-битное изображение к 8-битному
	ir_8bit = cv2.normalize(ir_image_16bit, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

	# 2. Преобразуем в 3 канала (все каналы равны) - это то же самое, что оттенки серого
	ir_3channel = cv2.cvtColor(ir_8bit, cv2.COLOR_GRAY2BGR)

	# Возвращаем 3-канальное изображение в оттенках серого
	return ir_3channel
