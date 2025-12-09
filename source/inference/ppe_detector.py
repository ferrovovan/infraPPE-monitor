# ppe_detector.py
from .ml.worker_detector import detect_workers
from .frame_process.cropper import crop_person
from .ml.ppe_classifier import detect_ppe_on_worker
from .bbox_convert import convert_ppe_bboxes
from .frame_process.drawer import draw_ppe
from .report.build_report import build_report
from .frame_process.ir_switch import switch_to_normal

from typing import Tuple
import numpy as np

from typing import Tuple
import numpy as np

# Архитектура модуля
# ppe_detector.py
# │   # take frame
# ├── detect_workers(frame) -> list[worker_bbox]
# ├── [cycle] crop_person(frame, worker_bbox) -> cropped_image
# ├── [cycle] detect_ppe_on_worker(cropped_image) -> list[bbox_ppe_rel]
# ├── [cycle] convert_ppe_bboxes(worker_ppe_rel_bboxes, worker_bbox) -> list[worker_ppe_bbox_absolute]
# ├── draw_ppe(frame, workers) -> frame_out
# │   # TODO: report
# ├── build_report(frame_id, workers) -> report
# │   #
# └── detect_ppe(frame_id, frame) -> frame_out, report
REQUIRED_PPE = ["Hardhat", "Mask"]


def ir_detect_ppe(frame_id: int, frame: np.ndarray):
	normal_frame = switch_to_normal(frame)
	return detect_ppe(frame_id, normal_frame)


def detect_ppe(frame_id: int, frame: np.ndarray) -> Tuple[np.ndarray, dict]:
	workers: list = detect_workers(frame)

	for worker in workers:
		worker["crop"] = crop_person(frame, worker["bbox"])
		
		worker["ppe_rel"] = detect_ppe_on_worker(worker["crop"])
		
		worker["ppe"] = convert_ppe_bboxes(worker["ppe_rel"], worker["bbox"])
	
	frame_out = draw_ppe(frame, workers)

	report = build_report(frame_id, workers, REQUIRED_PPE)

	return frame_out, report
