import streamlit as st
# DEVELOPMENT
import sys  # Для включения DEVEL
from pathlib import Path  # Для нахождения "test_input/{video}"
#
from ui.layout import render_header, render_futer
from ui.components import render_upload_panel
from run_modes.video_player import run_video_player
from run_modes.picture_show import run_picture_show

# Карта оркестратора
#   app.py
#   ├── Заголовок и шапка (строго, минималистично)
#   ├── Панель параметров
#   │   ├── загрузка видео
#   │   ├── выбор FPS
#   │   ├── «Запустить»
#   ├── Основной рабочий экран
#   │   ├── Левый блок — текущий кадр с метками
#   │   └── Правый блок — показатели системы:
#   │        • ppe_detected / нарушений
#   │        • время инференса
#   │        • статистика
#   ├── История событий
#   └── Футер


def init_state():
	# Инициализация состояний обработки
	if 'processing_state' not in st.session_state:
		st.session_state.processing_state = 'idle'  # 'idle', 'running', 'paused', 'stopped'
		st.session_state.pause_flag = False
		st.session_state.stop_flag = False


if __name__ == '__main__':
	init_state()
	render_header()

	params = render_upload_panel()

	# DEVEL 🗿shortcut🗿
	DEVEL = False
	user_args = sys.argv[1:]
	if user_args:
		DEVEL = ("devel" in user_args)
		params["infra_mode"] = ("infra_mode" in user_args)
	if DEVEL:
		params["start_button"] = True
		# params["infra_mode"] = True
		params["file_type"] = "picture"
		# params["file_type"] = "video"

		# Точно знаем что находимся здесь: "infraPPE-monitor")
		if params["file_type"] == "video":
			# DEVEL_FILE = "in.mp4"
			DEVEL_FILE = "Anthem_to_Workwear_and_Its_Protective_Role_in_the_RAP_Style.mp4"
		elif params["file_type"] == "picture":
			DEVEL_FILE = "KMZ_switch_shop.jpg"
		else:
			print("Сломался DEVEL")

		DEVEL_FILE_PATH = Path.cwd() / Path(f"test_input/{DEVEL_FILE}")
		params["file_path"] = str(DEVEL_FILE_PATH)
		open(DEVEL_FILE_PATH, 'rb')  # без открытия ничего не выйдет

	if params["start_button"]:
		if params["file_type"] == "picture":
			picture_params = {
				"picture_path": params["file_path"],
				"infra_mode": params["infra_mode"]
			}
			run_picture_show(**picture_params)
		elif params["file_type"] == "video":
			video_params = {
				"video_path": params["file_path"],
				"fps": params["fps"],
				"skip_frame_rate": params["skip_frame_rate"],
				"infra_mode": params["infra_mode"]
			}
			run_video_player(**video_params)
		else:
			st.text("Нет сценария запуска")

	render_futer()
