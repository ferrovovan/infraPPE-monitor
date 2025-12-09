import streamlit as st
import tempfile
import time
# DEVELOPMENT
import sys  # Для включения DEBUG
from pathlib import Path  # Для нахождения "test_input/in.mp4"
#
from inference_source import _frame_generator, _ir_frame_generator, _detect_ppe, _ir_detect_ppe

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

# # TODO
#  --- 1. Инициализация session_state ---
# if 'processing_state' not in st.session_state:
#     st.session_state.processing_state = 'idle'
#     # 'idle', 'running', 'stopped', 'completed'
#
#  --- 2. Функции обратного вызова ---
# def set_state_running():
#     st.session_state.processing_state = 'running'
#
# def set_state_stopped():
#     st.session_state.processing_state = 'stopped'
#
# # TODO
#  --- История ---
# if "history" not in st.session_state:
# 	st.session_state.history = []
#
# if "stats" not in st.session_state:
# 	st.session_state.stats = {
# 		"total": 0,
# 		"helmet_no": 0,
# 		"mask_no": 0,
# 		"critical": 0
# 	}
#
# =============================
#      ЗАГОЛОВОК И ШАПКА
# =============================

# === Настройка страницы ===
st.set_page_config(
	page_title="CV-10 | Контроль СИЗ в ИК-диапазоне",
	page_icon="helmet",  # обычный эмодзи — работает
	layout="wide"
)

# === Стили ===
st.markdown("""
<style>
	.big-font {font-size: 42px !important;
	 font-weight: bold; color: #1E3A8A;}
	.risk-low {background-color: #DCFCE7; padding: 20px;
	 border-radius: 12px; border-left: 6px solid #22C55E;}
	.risk-medium {background-color: #FEF3C7; padding: 20px;
	 border-radius: 12px; border-left: 6px solid #F59E0B;}
	.risk-high {background-color: #FEE2E2; padding: 20px;
	 border-radius: 12px; border-left: 6px solid #EF4444;}
	.header-box {
		background: linear-gradient(90deg, #1E3A8A, #3B82F6);
		padding: 25px;
		border-radius: 15px;
		color: white;
		text-align: center;
	}
</style>
""", unsafe_allow_html=True)

# шапка
header_html = """
<div class="header-box">
    <h1>CV-10: ИИ-контроль СИЗ</h1>
    <p>Работает в полной темноте, дыму и тумане</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
# st.title("PPE Monitor — Prototype")
st.markdown("---")


# =============================
#      ПАНЕЛЬ ПАРАМЕТРОВ
# =============================

video = st.file_uploader("Загрузите видео", type=["mp4", "mkv"])
fps = st.slider("Скорость воспроизведения (кадров/сек)", 1, 30, 2)
skip_frame_rate = st.slider("skip frames rate", 0, 60, 15)
infra_mode = st.checkbox("Enable infrared mode")
start_button = st.button("▶ Запустить обработку")


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
	#DEVEL_FILE_PATH = Path.cwd() / Path("test_input/in.mp4")
	DEVEL_FILE_PATH = Path.cwd() / Path("test_input/Anthem_to_Workwear_and_Its_Protective_Role_in_the_RAP_Style.mp4")
	video = open(DEVEL_FILE_PATH, 'rb')


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


def update_metrics(placeholder, report: dict, inf_time: float):
	# Используем with placeholder: для очистки контейнера и замены содержимого
	with placeholder:
		st.markdown("### Показатели")
		st.metric("Инференс (мс)", f"{inf_time * 1000:.1f}")
		st.markdown("### Отчёт")
		st.write(report)


def save_temp_video():
	# Сохраняем видео во временный файл
	temp_video_path = tempfile.NamedTemporaryFile(
		delete=False  # , suffix=".mp4"
	)
	temp_video_path.write(video.read())
	temp_video_path.close()
	return temp_video_path.name


if start_button and video:
	if DEVEL:
		video_path = DEVEL_FILE_PATH
	else:
		video_path = save_temp_video()

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

	total_frames = 1000  # ЗАГЛУШКА
	start_time = time.time()

	if infra_mode:
		frame_gen = _ir_frame_generator(video_path, skip_frame_rate)
		run_inference = _ir_detect_ppe
	else:
		frame_gen = _frame_generator(video_path, skip_frame_rate)
		run_inference = _detect_ppe

	# обработка по кадрово
	for frame_id, frame in frame_gen:
		# Обработка кадра
		t0 = time.time()
		frame_out, report = run_inference(frame_id, frame)
		t1 = time.time()

		# Обновление блоков
		update_frame(frame_placeholder, frame_out, frame_id)
		update_metrics(metrics_placeholder, report, t1 - t0)

	        # Полоса прогресса под колонками
		progress.progress((frame_id + 1) / total_frames)

		# Задержка, чтобы не нагружать.
		time.sleep(1.0 / fps)

	total_time = time.time() - start_time
	st.success("Обработка завершена за {total_time:.1f} секунд!")


# =============================
#     ИСТОРИЯ СОБЫТИЙ
# =============================
#
# TODO
# === История ===
# if st.session_state.history:
#	st.markdown("---")
#	st.markdown("### История проверок")
#	st.dataframe(
#               st.session_state.history[-10:][::-1],
#               use_container_width=True, hide_index=True
#       )

# =============================
#     ПОДВАЛ СТРАНИЦЫ
# =============================

# === Футер ===
st.markdown("---")
st.markdown(
	"<p style='text-align: center; color: grey;'>"
	"CV-10 • ИИ-контроль СИЗ в ИК-диапазоне"  # • Работает без интернета
	"</p>",
	unsafe_allow_html=True
)
