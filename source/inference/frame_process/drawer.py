# drawer.py
import cv2
import numpy as np
from typing import Tuple, NamedTuple, Optional
from ..bbox_types import dBBox, Worker


# Именованный кортеж
class Point(NamedTuple):
	x: int
	y: int


def bbox_points(bbox: dBBox) -> Tuple[Point, Point]:
	"""Преобразует bounding box в две точки (верхний левый и нижний правый угол)."""
	p1 = Point(int(bbox["x1"]), int(bbox["y1"]))
	p2 = Point(int(bbox["x2"]), int(bbox["y2"]))
	return (p1, p2)


class Drawer:
	"""
	Класс для рисования bounding boxes и текста на изображениях.
	"""
	
	def __init__(self, scale_factor: float):
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.font_scale = 0.8 * scale_factor
		# Толщина шрифта:  пропорциональна scale_factor
		self.font_thickness = int(1 * scale_factor)
		# Толщина рамки: чуть больше толщины шрифта
		self.box_thickness = int(4.0 * scale_factor)
		
		# Отступы и смещения тоже масштабируются
		self.text_padding = int(5 * scale_factor)
		self.text_vertical_offset = int(25 * scale_factor)

		# Цвета
		self.text_bg_color = (255, 0, 0)   # Синий фон под текстом
		self.text_color = (255, 255, 255)  # Белый текст
		self.worker_color = (255, 0, 0)    # Синий для рабочих
		self.ppe_color = (0, 255, 0)       # Зеленый для СИЗ

	def _calculate_text_position(self, coords: Tuple[Point, Point]) -> Tuple[int, int]:
		"""
		Вычисляет позицию для текста над bounding box.
		
		Args:
			coords: Кортеж из двух точек (p1, p2) bounding box
			
		Returns:
			Кортеж (x, y) - верхний центр для текста
		"""
		p1, p2 = coords
		x_center = (p1.x + p2.x) // 2
		y_top = p1.y - self.text_vertical_offset
		0 if y_top < 0 else y_top
		return (x_center, y_top)

	def _draw_text_with_background(self, frame: np.ndarray, text: str, 
		position: Tuple[int, int]
	) -> np.ndarray:
		"""
		Рисует текст с фоном для лучшей читаемости.
		
		Args:
			frame: Изображение для рисования
			text: Текст для отображения
			position: Кортеж (x, y) - желаемая позиция текста (верхний центр)
			
		Returns:
			Изображение с нарисованным текстом
		"""
		# Получаем размеры текста
		(text_width, text_height), baseline = cv2.getTextSize(
			text, self.font, self.font_scale, self.font_thickness
		)
		
		# Вычисляем координаты фона
		x_center, y_top = position
		text_x = x_center - text_width // 2
		text_y = y_top + text_height + baseline
		
		# Координаты фона
		bg_x1 = text_x - 5
		bg_y1 = y_top - 5
		bg_x2 = text_x + text_width + 5
		bg_y2 = text_y + baseline + 5
		
		# Рисуем фон
		cv2.rectangle(frame, (bg_x1, bg_y1), (bg_x2, bg_y2), 
					self.text_bg_color, -1)
		
		# Рисуем текст
		cv2.putText(frame, text, (text_x, text_y),
				self.font, self.font_scale, self.text_color,
				self.font_thickness, cv2.LINE_AA)
		
		return frame

	def draw_bbox(self, frame: np.ndarray, coords: Tuple[Point, Point], 
		color: Tuple[int, int, int]
	) -> np.ndarray:
		"""
		Рисует bounding box на изображении.
		
		Args:
			frame: Изображение для рисования
			coords: Кортеж из двух точек (p1, p2)
			color: Цвет рамки в формате BGR
			thickness: Толщина линии
			
		Returns:
			Изображение с нарисованной рамкой
		"""
		cv2.rectangle(frame, coords[0], coords[1], color, self.box_thickness)
		return frame

	def draw_worker(self, frame: np.ndarray, coords: Tuple[Point, Point], 
					worker_id: int) -> np.ndarray:
		"""
		Рисует bounding box рабочего и его ID.
		
		Args:
			frame: Изображение для рисования
			coords: Координаты bounding box
			worker_id: ID рабочего
			
		Returns:
			Изображение с нарисованным рабочим
		"""
		# Рисуем рамку
		frame = self.draw_bbox(frame, coords, self.worker_color)
		
		# Рисуем текст с ID
		text = f"Worker ID: {worker_id}"
		text_position = self._calculate_text_position(coords)
		frame = self._draw_text_with_background(frame, text, text_position)
		
		return frame

	def draw_ppe(self, frame: np.ndarray, coords: Tuple[Point, Point], 
				ppe_label: Optional[str] = None) -> np.ndarray:
		"""
		Рисует bounding box СИЗ и метку.
		
		Args:
			frame: Изображение для рисования
			coords: Координаты bounding box
			ppe_label: Метка СИЗ (например, 'helmet', 'vest')
			
		Returns:
			Изображение с нарисованным СИЗ
		"""
		# Рисуем рамку
		frame = self.draw_bbox(frame, coords, self.ppe_color)
		
		# Рисуем текст с меткой СИЗ
		if ppe_label:
			text = f"PPE: {ppe_label}"
			text_position = self._calculate_text_position(coords)
			# Смещаем текст немного вниз, чтобы не перекрывать рамку рабочего
			text_position = (text_position[0], text_position[1])
			frame = self._draw_text_with_background(frame, text, text_position)
		
		return frame


def calc_image_scale_factor(frame: np.ndarray) -> int:
	"""
	Упрощенная версия: вычисляет толщину на основе площади изображения.
	
	Args:
		frame: Входное изображение
		
	Returns:
		int: Толщина линии (1, 2, 3 или 4)
	"""
	height, width = frame.shape[:2]
	area = height * width
	
	# Определяем толщину на основе площади изображения
	if area < 300 * 300:  # Маленькие изображения
		return 1
	elif area < 800 * 800:  # Средние изображения
		return 2
	elif area < 1500 * 1500:  # Большие изображения
		return 3
	elif area < 1800 * 1800:  # Очень большие изображения
		return 4
	else:  # Остальные
		return 5


def draw_ppe(frame: np.ndarray, workers: list[Worker]) -> np.ndarray:
	"""
	Рисует рамки рабочих и их СИЗ на кадре.
	
	Args:
		frame: Исходное изображение
		workers: Список рабочих с их bounding boxes и СИЗ
		
	Returns:
		Изображение с нарисованными рамками и текстами
	"""
	out_frame = frame.copy()
	scale_factor = calc_image_scale_factor(frame)
	drawer = Drawer(scale_factor)
	
	for worker in workers:
		worker_coords = bbox_points(worker["bbox"])
		out_frame = drawer.draw_worker(out_frame, worker_coords, worker['id'])
		
		for ppe in worker["ppe"]:
			ppe_coords = bbox_points(ppe)
			ppe_label = ppe.get("label")
			out_frame = drawer.draw_ppe(out_frame, ppe_coords, ppe_label)
	
	return out_frame
