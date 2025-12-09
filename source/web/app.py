import streamlit as st
# DEVELOPMENT
import sys  # Для включения DEVEL
from pathlib import Path  # Для нахождения "test_input/{video}"
#
from ui.layout import render_header, render_futer
from ui.components import render_upload_panel
from player.player import run_player

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

# =============================
#      ИНИЦИАЛИЗАЦИЯ st.session_state
# =============================
#
# st.session_state - это оперативная память сеанса

# Инициализация состояний обработки
if 'processing_state' not in st.session_state:
	st.session_state.processing_state = 'idle'  # 'idle', 'running', 'paused', 'stopped'
	st.session_state.pause_flag = False
	st.session_state.stop_flag = False

# =============================
#     КОЛЛБЭКИ ДЛЯ УПРАВЛЕНИЯ ПРОИГРЫВАТЕЛЕМ
# =============================


def pause_processing():
    """Поставить обработку на паузу"""
    if st.session_state.processing_state == 'running':
        st.session_state.processing_state = 'paused'
        st.session_state.pause_flag = True
    elif st.session_state.processing_state == 'paused':
        st.session_state.processing_state = 'running'
        st.session_state.pause_flag = False


def stop_processing():
    """Полностью остановить обработку"""
    st.session_state.processing_state = 'stopped'
    st.session_state.stop_flag = True
    st.session_state.pause_flag = False


# =============================
#      ЗАГОЛОВОК И ШАПКА
# =============================
render_header()


# =============================
#      ПАНЕЛЬ ПАРАМЕТРОВ
# =============================
video, fps, skip_frame_rate, infra_mode, start_button, pause_button, stop_button = render_upload_panel()


# =============================
#     DEVEL config
# =============================
DEVEL = False
user_args = sys.argv[1:]
if user_args:
	DEVEL = ("devel" in user_args)
	infra_mode = ("infra_mode" in user_args)

if DEVEL:
	start_button = True
	# infra_mode = True
	# Точно знаем что находимся здесь: "infraPPE-monitor")
	# DEVEL_FILE_PATH = Path.cwd() / Path("test_input/in.mp4")  # Old test input
	DEVEL_FILE_PATH = Path.cwd() / Path("test_input/Anthem_to_Workwear_and_Its_Protective_Role_in_the_RAP_Style.mp4")
	video = open(DEVEL_FILE_PATH, 'rb')
else:
	DEVEL_FILE_PATH = ""


# =============================
#     ОСНОВНОЙ РАБОЧИЙ ЭКРАН
# =============================
run_player(video, fps, skip_frame_rate, infra_mode, start_button, DEVEL, DEVEL_FILE_PATH)


# =============================
#     ПОДВАЛ СТРАНИЦЫ
# =============================
render_futer()
