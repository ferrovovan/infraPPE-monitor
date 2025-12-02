# cropper.py
import numpy as np
from ..bbox_types import dBBox


def crop_person(frame: np.ndarray, bbox: dBBox) -> np.ndarray:
	"""
	Возвращает обрезок изображения по bbox.
	"""
	return frame[bbox["y1"]:bbox["y2"], bbox["x1"]:bbox["x2"]].copy()
