# picture_show.py
import streamlit as st
import time
#
from .inference_source import _picture_taker, _ir_picture_taker, _detect_ppe, _ir_detect_ppe


def update_frame(placeholder, frame):
	with placeholder:
		placeholder.image(
			frame,
			channels="BGR"
		)


def update_metrics(placeholder, html_report, inf_time: float):
	with placeholder:
		st.markdown("### Показатели")
		st.metric("Инференс (мс)", f"{inf_time * 1000:.1f}")
		st.markdown("### Отчёт")
		st.html(report)


def run_picture_show(picture_path, infra_mode):
	# окошки
	col_left, col_right = st.columns([1.3, 1])
	with col_left:
		frame_placeholder   = st.empty()  # область для "кадра"
	with col_right:
		metrics_placeholder = st.empty()  # область для статистик

	if infra_mode:
		pict_take = _picture_taker
		run_pict_inference = _ir_detect_ppe
	else:
		pict_take = _ir_picture_taker
		run_pict_inference = _detect_ppe

	frame = pict_take(picture_path)
	# Обработка "кадра"
	int_start_time = time.time()
	frame_out, html_report = run_pict_inference(1, frame)
	inference_time = time.time() - int_start_time

	# Обновление блоков
	update_frame(frame_placeholder, frame_out)
	update_metrics(metrics_placeholder, html_report, inference_time)
