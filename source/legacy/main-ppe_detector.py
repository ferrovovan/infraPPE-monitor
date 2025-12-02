# from .ml/worker_detector import detect_workers
#from .frame_process/cropper import crop_with_bbox
#from .ml/ppe_classifier import detect_ppe
#from .bbox_mapper import map_local_to_global
#from .frame_process/drawer import draw_ppe

# Архитектура модуля
# ppe_detector.py
# │   # take frame
# ├── detect_workers(frame) -> list[worker_bbox]
# ├── [cycle] crop_people(frame, bboxes_people) -> list[cropped_images]
# ├── detect_ppe_on_worker(cropped_image) -> list[bbox_ppe_rel]
# ├── convert_ppe_bboxes(ppe_rel_bboxes, worker_bbox) -> list[bbox_ppe_absolute]
# ├── [cycle] draw_ppe(frame, absolute_ppe_bboxes) -> frame_out
# │   # TODO: create report
# └── detect_ppe(frame_id, frame) -> frame_out, report


def detect_ppe(frame_id, frame):
	"""
	Главная функция обработки кадра.
	Возвращает:
		processed_frame, report: dict
	"""

	persons = detect_workers(frame)

	all_global_ppe = []
	people_info = []

	for pid, pb in enumerate(persons):
		# 1) Вырезаем человек
		crop = crop_person(frame, pb)

		# 2) PPE внутри вырезки
		local_items = detect_local_ppe(crop)

		# 3) Переводим в глобальные координаты
		global_items = map_local_to_global(pb, local_items)

		# Для визуализации накопим все найденные PPE
		all_global_ppe.extend(global_items)

		# 4) Формируем описание конкретного человека
		people_info.append({
			"frame_id": frame_id,
			"person_id": pid,
			"person_bbox": pb,
			"ppe": summarize_ppe(local_items),
			"ppe_items": global_items,
		})

	# 5) Визуализация
	processed_frame = draw_ppe(frame, all_global_ppe)

	# 6) Итоговый объект
	result = {
		"frame_id": frame_id,
		"people": people_info
	}

	return processed_frame, result


def summarize_ppe(local_items):
	"""
	Упрощённая сводка по PPE.
	"""
	classes = {item["cls"] for item in local_items}
	return {
		"helmet": "helmet" in classes,
		"gloves": "gloves" in classes,
		"mask":   "mask"   in classes
	}


from .person_detector import detect_people
from .cropper import crop_person
from .ppe_detector_sub import detect_ppe_on_person
from .bbox_convert import convert_ppe_bboxes
from .drawer import draw_ppe
import numpy as np

def detect_ppe(frame_id, frame) -> (np.ndarray, dict):
	report = {"frame_id": frame_id, "people": []}

	# 1. Детект людей
	people_bboxes = detect_people(frame)

	for person_id, bbox in enumerate(people_bboxes):
		crop = crop_person(frame, bbox)

		# 2. Детект PPE внутри кропа
		ppe_rel = detect_ppe_on_person(crop)

		# 3. Конвертация в абсолютные координаты
		ppe_abs = convert_ppe_bboxes(ppe_rel, bbox)

		# 4. Добавление в отчёт
		report["people"].append({
			"id": person_id,
			"bbox": bbox,
			"crop": crop,      # можно не сохранять если требует памяти
			"ppe": ppe_abs,
		})

	# 5. Рисование
	frame_out = draw_ppe(frame, report["people"])

	return frame_out, report
