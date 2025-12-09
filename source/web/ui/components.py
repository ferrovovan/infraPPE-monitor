import streamlit as st
from .state_manager import pause_processing, stop_processing


def render_upload_panel():
	video = st.file_uploader("Загрузите видео", type=["mp4", "mkv"])
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
	pause_button = st.button(
		"⏸ Приостановить обработку",
		key="pause_button",
		on_click=pause_processing)
	stop_button = st.button(
		"⏹ Остановить обработку",
		key="stop_button",
		on_click=stop_processing)
	return video, fps, skip_frame_rate, infra_mode, start_button, pause_button, stop_button
