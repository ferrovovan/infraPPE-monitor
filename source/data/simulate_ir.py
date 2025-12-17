# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# simulate_ir.py

import cv2
import numpy as np


def rgb_to_ir(rgb_frame: np.ndarray) -> np.ndarray:
	"""
	Имитирует ИК-изображение из RGB.
	Возвращает одноканальное 16-битное изображение (тип uint16).
	"""
	# Преобразуем в оттенки серого (8 бит)
	gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
	
	# Масштабируем до 16 бит (0-65535) и нормализуем
	# Используем разные коэффициенты для имитации ИК-характеристик
	ir_16bit = (gray.astype(np.float32) * 257).astype(np.uint16)

	# Имитируем ИК-характеристики: усиливаем темные области
	# (в ИК-изображениях обычно лучше видны теплые объекты)
	ir_16bit = cv2.normalize(ir_16bit, None, 0, 65535, cv2.NORM_MINMAX)

	return ir_16bit
