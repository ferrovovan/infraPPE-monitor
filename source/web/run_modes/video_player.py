# player.py
import streamlit as st
import time
#
from .inference_source import (
	_frame_generator,
	_ir_frame_generator,
	_detect_ppe,
	_ir_detect_ppe
)


# =============================
#     ОСНОВНОЙ РАБОЧИЙ ЭКРАН
# =============================

def update_frame(placeholder, frame, frame_id: int):
	with placeholder:
		placeholder.image(
			frame,
			caption=f"Кадр {frame_id}",
			channels="BGR"
		)


def update_metrics(placeholder, html_report: str, inf_time: float):
	# Используем with placeholder: для очистки контейнера и замены содержимого
	with placeholder:
		st.markdown("### Показатели")
		st.metric("Инференс (мс)", f"{inf_time * 1000:.1f}")
		st.markdown("### Отчёт")
		st.html(html_report)


def run_video_player(video_path, fps, skip_frame_rate, infra_mode):
	# окошки
	col_left, col_right = st.columns([1.3, 1])
	with col_left:
		frame_placeholder   = st.empty()  # область для обновления кадра
	with col_right:
		metrics_placeholder = st.empty()  # область для статистик

	# TODO: Остановка цикла, без "отмены" start_button
	# Нажатие кнопки (в Steamlit) перезапускает весь скрипт,
	# отменяя прошлое состояние start_button.
	# Поэтому необходимо применять  `st.session_state`
	#
	# pause_button = st.button("⏸ Приостановить обработку")
	# stop_button = st.button("⏹ Остановить обработку")

	progress = st.progress(0)   # полоса прогресса

	st.session_state.processing_state = 'running'
	st.session_state.pause_flag = False
	st.session_state.stop_flag = False

	total_frames = 1000         # ЗАГЛУШКА
	start_time = time.time()

	if infra_mode:
		frame_gen = _ir_frame_generator(video_path, skip_frame_rate)
		run_inference = _ir_detect_ppe
	else:
		frame_gen = _frame_generator(video_path, skip_frame_rate)
		run_inference = _detect_ppe

	# обработка по кадрово
	for frame_id, frame in frame_gen:
		if st.session_state.stop_flag:
			st.info("Обработка остановлена пользователем")
			break
		# Обработка кадра
		int_start_time = time.time()
		frame_out, html_report = run_inference(frame_id, frame)
		inference_time = time.time() - int_start_time

		# Обновление блоков
		update_frame(frame_placeholder, frame_out, frame_id)
		update_metrics(metrics_placeholder, html_report, inference_time)

		# Полоса прогресса под колонками
		progress.progress((frame_id + 1) / total_frames)

		# Задержка, чтобы не нагружать.
		if inference_time < fps:
			time.sleep(fps - inference_time)

	total_time = time.time() - start_time
	st.success(f"Обработка завершена за {total_time:.1f} секунд!")
