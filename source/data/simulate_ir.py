import cv2


def rgb_to_ir(rgb_frame):
	"""
	Простая заглушка для имитирования ИК-изображений
	"""
	# TODO: Правильное ИК-изображение  бит.
	# ИК-кадр - это 1 канал 12/16
	# А сейчас выдаётся цветное изображение - псевдо-RGB (3 канала, 8 бит)
	# Это не правильно!
	gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
	ir_sim = cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
	return ir_sim
