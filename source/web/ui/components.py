# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# components.py

import streamlit as st
import tempfile
# from .state_manager import pause_processing, stop_processing


def save_temp_file(f):
	"""
	Сохранение во временный файл
	"""
	temp_file_path = tempfile.NamedTemporaryFile(
		delete=False  # , suffix=".extension"
	)
	temp_file_path.write(f.read())
	temp_file_path.close()
	return temp_file_path.name


# =============================
#      ПАНЕЛЬ ПАРАМЕТРОВ
# =============================
def render_upload_panel():
	video = st.file_uploader("Загрузите видео", type=["mp4", "mkv"])
	picture = st.file_uploader("Загрузите картинку", type=["png", "jpg", "tiff", "bmp"])
	fps = st.slider(
		"Скорость воспроизведения (сек/кадр)",
		min_value=0.0,
		max_value=10.0,
		value=2.0,
		step=0.2
	)
	skip_frame_rate = st.slider("skip frames rate", 0, 60, 10)
	infra_mode = st.checkbox("Enable infrared mode")

	start_button = st.button("▶ Запустить обработку")
	# pause_button = st.button(
	#	"⏸ Приостановить обработку",
	#	key="pause_button",
	#	on_click=pause_processing)
	# stop_button = st.button(
	#	"⏹ Остановить обработку",
	#	key="stop_button",
	#	on_click=stop_processing)

	# Превращаем вход в temp-файл, если он загружен.
	file_path = None
	file_type = None
	if video is not None:
		file_type = "video"
		file_path = save_temp_file(video)
	elif picture is not None:
		file_type = "picture"
		file_path = save_temp_file(picture)

	return {
		"file_path": file_path,
		"file_type": file_type,
		"fps": fps,
		"skip_frame_rate": skip_frame_rate,
		"infra_mode": infra_mode,
		"start_button": start_button,
		# "pause_button": pause_button,
		# "stop_button": stop_button
	}
