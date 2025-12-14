# load_video.py

import cv2
from .simulate_ir import rgb_to_ir


def _base_video_generator(video_path: str, skip_rate: int = 1):
	"""
	Генератор кадров с индексом.
	Возвращает пары (номер кадра, изображение np.ndarray)
	"""
	if skip_rate < 1:
		raise ValueError(f"skip_rate должен быть >= 1, получено: {skip_rate}")

	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened():
		raise ValueError(f"Не удалось открыть видео: {video_path}")

	idx = 0
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		
		# # Пропускаем кадры в соответствии с skip_rate
		if idx % skip_rate == 0:
			yield idx, frame

		idx += 1
	cap.release()


def frame_generator(video_path: str, skip_rate: int = 1):
	"""
	Публичный генератор стандартных (BGR/RGB) кадров.
	"""
	yield from _base_video_generator(video_path, skip_rate)


def ir_frame_generator(video_path: str, skip_rate: int = 1):
	"""
	Публичный генератор симуляции ИК-кадров. Применяет трансформацию.
	"""
	for idx, frame in _base_video_generator(video_path, skip_rate):
		ir_frame = rgb_to_ir(frame)
		yield idx, ir_frame
