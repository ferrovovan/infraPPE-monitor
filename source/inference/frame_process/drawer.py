# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
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
	
	def __init__(self):
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		# Базовые значения без масштабирования
		self.font_scale_base = 0.3
		self.font_thickness_base = 0.7
		self.box_thickness_base = 2.0
		self.text_padding_base = 1
		self.text_vertical_offset_base = 20

		# Цвета
		self.text_bg_color = (255, 0, 0)   # Синий фон под текстом
		self.text_color = (255, 255, 255)  # Белый текст
		self.worker_color = (255, 0, 0)    # Синий для рабочих
		self.ppe_color = (0, 255, 0)       # Зеленый для СИЗ

	@staticmethod
	def calc_coords_scale_factor(coords: Tuple[Point, Point]) -> float:
		"""
		Вычисляет масштабный коэффициент на основе размера bounding box.
		Относительный подсчет: коэффициент зависит от размера бокса.

		Args:
		    coords: Кортеж из двух точек (p1, p2) bounding box
		    
		Returns:
		    float: Масштабный коэффициент (0.5-2.0)
		"""
		p1, p2 = coords
		width = abs(p2.x - p1.x)
		height = abs(p2.y - p1.y)

		# Вычисляем площадь bounding box
		area = width * height

		# Нормализуем площадь относительно эталонного размера (100x100 пикселей)
		# Эталонный размер можно настроить в зависимости от типичных размеров объектов
		reference_area = 100 * 100

		# Относительный масштабный коэффициент
		# Используем квадратный корень для линейной зависимости от размера
		scale_factor = max(0.5, min(2.0, np.sqrt(area / reference_area)))

		return scale_factor

	def _calculate_text_position(self, coords: Tuple[Point, Point], scale_factor: float) -> Tuple[int, int]:
		"""
		Вычисляет позицию для текста над bounding box.
		
		Args:
			coords: Кортеж из двух точек (p1, p2) bounding box
			
		Returns:
			Кортеж (x, y) - верхний центр для текста
		"""
		p1, p2 = coords
		x_center = (p1.x + p2.x) // 2
		y_top = p1.y - int(self.text_vertical_offset_base * scale_factor)
		return (x_center, y_top)

	def _draw_text_with_background(self, frame: np.ndarray, text: str, 
		position: Tuple[int, int], scale_factor: float
	) -> np.ndarray:
		"""
		Рисует текст с фоном для лучшей читаемости.
		
		Args:
			frame: Изображение для рисования
			text: Текст для отображения
			position: Кортеж (x, y) - желаемая позиция текста (верхний центр)
			scale_factor: Масштабный коэффициент для данного bounding box
			
		Returns:
			Изображение с нарисованным текстом
		"""
		font_scale = self.font_scale_base * scale_factor
		font_thickness = int(self.font_thickness_base * scale_factor)

		# Получаем размеры текста
		(text_width, text_height), baseline = cv2.getTextSize(
			text, self.font, font_scale, font_thickness
		)
		
		# Вычисляем координаты фона
		x_center, y_top = position
		text_x = x_center - text_width // 2
		text_y = y_top + text_height + baseline
		
		# Масштабируем отступы фона
		padding = int(self.text_padding_base * scale_factor)
		bg_x1 = text_x - padding
		bg_y1 = y_top - padding
		bg_x2 = text_x + text_width + padding
		bg_y2 = text_y + baseline + padding
		
		# Рисуем фон
		cv2.rectangle(frame, (bg_x1, bg_y1), (bg_x2, bg_y2), 
					self.text_bg_color, -1)
		
		# Рисуем текст
		cv2.putText(frame, text, (text_x, text_y),
				self.font, font_scale, self.text_color,
				font_thickness, cv2.LINE_AA)
		
		return frame

	def draw_bbox(self, frame: np.ndarray, coords: Tuple[Point, Point], 
		color: Tuple[int, int, int], scale_factor: float
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
		box_thickness = int(self.box_thickness_base * scale_factor)
		cv2.rectangle(frame, coords[0], coords[1], color, box_thickness)
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
		# Коэффициент обозначения
		scale_factor: float = self.calc_coords_scale_factor(coords)

		# Рисуем рамку
		frame = self.draw_bbox(frame, coords, self.worker_color, scale_factor)
		
		# Рисуем текст с ID
		text = f"Worker ID: {worker_id}"
		text_position = self._calculate_text_position(coords, scale_factor)
		frame = self._draw_text_with_background(frame, text, text_position, scale_factor)
		
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
		# Коэффициент обозначения
		scale_factor: float = self.calc_coords_scale_factor(coords)
		
		# Рисуем рамку
		frame = self.draw_bbox(frame, coords, self.ppe_color, scale_factor)
		
		# Рисуем текст с меткой СИЗ
		if ppe_label:
			text = f"PPE: {ppe_label}"
			text_position = self._calculate_text_position(coords, scale_factor)
			# Смещаем текст немного вниз, чтобы не перекрывать рамку рабочего
			text_position = (text_position[0], text_position[1])
			frame = self._draw_text_with_background(frame, text, text_position, scale_factor)
		
		return frame


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
	drawer = Drawer()
	
	for worker in workers:
		worker_coords = bbox_points(worker["bbox"])
		out_frame = drawer.draw_worker(out_frame, worker_coords, worker['id'])
		
		for ppe in worker["ppe"]:
			ppe_coords = bbox_points(ppe)
			ppe_label = ppe.get("label")
			out_frame = drawer.draw_ppe(out_frame, ppe_coords, ppe_label)
	
	return out_frame
