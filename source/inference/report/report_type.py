# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# report_type.py
from typing import TypedDict, List


class WorkerReport(TypedDict):
	"""
	Семантическая сводка по одному работнику.
	"""
	id: int                   # Уникальный идентификатор работника на кадре
	present: List[str]        # Список СИЗ, которые обнаружены и считаются корректными
	missing: List[str]        # Список обязательных СИЗ, которые отсутствуют


class FrameSummary(TypedDict):
	"""
	Итоговая статистика по кадру.
	"""
	workers_count: int        # Всего работников на кадре
	violations_count: int     # Сколько работников нарушают требования


class Report(TypedDict):
	"""
	Общий отчёт для одного кадра.
	Должен быть прост в восприятии, не содержать внутренних признаков модели.
	"""
	frame_id: int
	workers: List[WorkerReport]
	summary: FrameSummary
