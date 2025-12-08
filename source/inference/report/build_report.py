# build_report.py
from typing import Dict, List
from ..bbox_types import Worker
from .report_type import Report, FrameSummary, WorkerReport

# Можно вынести конфиг в другое место
DEFAULT_REQUIRED_PPE = ["Hardhat", "Safety Vest", "Gloves", "Goggles", "Mask"]
NO_PREFIX = "NO-"


def build_report(
	frame_id: int,
	workers: List[Worker],
	required_ppe: List[str] | None = None
) -> Dict:
	"""
	Формирует аналитический отчёт по кадру.
	Логика:
	- Для каждого рабочего вычисляется статус всех СИЗ.
	- 'NO-class' имеет приоритет отрицания.
	- Возвращается компактная структура:
		* данные по людям
		* агрегированные отсутствующие СИЗ
	"""

	# 1. Инициализация
	if required_ppe is None:
		required_ppe = DEFAULT_REQUIRED_PPE

	# 2. Обработка работников
	people_reports = []
	violation_count = 0

	for w in workers:
		worker_id = w["id"]

		# Собираем все подписи PPE, которые модель дала
		detected_ppe = [bb["label"] for bb in w["ppe"] if bb.get("label")]

		# Логическая оценка наличия обязательных СИЗ
		present_flags: Dict[str, bool] = {}

		for ppe_name in required_ppe:
			pos = ppe_name                # например: "Hardhat"
			neg = NO_PREFIX + ppe_name    # например: "NO-Hardhat"

			has_pos = pos in detected_ppe
			has_neg = neg in detected_ppe

			# Правило приоритета отрицания
			if has_neg:
				present_flags[ppe_name] = False
			else:
				present_flags[ppe_name] = bool(has_pos)

		# Какие обязательные СИЗ отсутствуют
		missing = [name for name, ok in present_flags.items() if not ok]
		if missing:
			violation_count += 1

		# Формируем WorkerReport
		worker_report: WorkerReport = {
			"id": worker_id,
			"present": [name for name, ok in present_flags.items() if ok],
			"missing": missing
		}

		people_reports.append(worker_report)

	# 3. Итоговая сводка
	summary: FrameSummary = {
		"total": len(workers),
		"violations": violation_count
	}

	# Итоговая структура Report
	report: Report = {
		"frame_id": frame_id,
		"workers": people_reports,
		"summary": summary
	}

	return report

# Пример выхода
# {
#     "frame_id": 123,
#     "people": [
#         {
#             "id": 1,
#             "present": ["Hardhat", "Gloves"],
#             "missing": ["Goggles", "Mask"]
#         },
#         ...
#     ],
#     "summary": {
#         "total": 5,
#         "violations": 2
#     }
# }
