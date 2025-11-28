import streamlit as st
import tempfile
import threading
import time
from inference_source import generate_frames, run_inference

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
#
# st.session_state - это оперативная память сеанса


# --- Инициализация состояния ---
if "history" not in st.session_state:
	st.session_state.history = []

if "stats" not in st.session_state:
	st.session_state.stats = {
		"total": 0,
		"helmet_no": 0,
		"mask_no": 0,
		"critical": 0
	}

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
	.big-font {font-size: 42px !important; font-weight: bold; color: #1E3A8A;}
	.risk-low {background-color: #DCFCE7; padding: 20px; border-radius: 12px; border-left: 6px solid #22C55E;}
	.risk-medium {background-color: #FEF3C7; padding: 20px; border-radius: 12px; border-left: 6px solid #F59E0B;}
	.risk-high {background-color: #FEE2E2; padding: 20px; border-radius: 12px; border-left: 6px solid #EF4444;}
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
st.markdown('<div class="header-box"><h1>CV-10: ИИ-контроль СИЗ</h1><p>Работает в полной темноте, дыму и тумане</p></div>', unsafe_allow_html=True)
#st.title("PPE Monitor — Prototype")
st.markdown("---")


# =============================
#      ПАНЕЛЬ ПАРАМЕТРОВ
# =============================

video = st.file_uploader("Загрузите видео", type=["mp4", "mkv"])
fps = st.slider("Скорость воспроизведения (кадров/сек)", 1, 30, 2)
st.checkbox("Enable infrared mode")
start_button = st.button("▶ Запустить обработку")


# =============================
#     ОСНОВНОЙ РАБОЧИЙ ЭКРАН
# =============================

def update_frame(placeholder, frame, frame_id: int, res: dict):
	with placeholder:
		placeholder.image(
			frame,
			caption=f"Кадр {frame_id}: {res['ppe_detected']}",
			channels="BGR"
		)

def update_metrics(placeholder, res: dict, inf_time: float):
	# Используем with placeholder: для очистки контейнера и замены содержимого
	with placeholder:
		st.markdown("### Показатели")
		st.metric("Инференс (мс)", f"{inf_time*1000:.1f}")
		st.metric("Обнаружено", res['ppe_detected'])

# 1. Функция, которая будет работать в отдельном потоке
def process_video_in_background(video_path, total_frames):
	for frame_id, frame in generate_frames(video_path):
		t0 = time.time()
		res = run_inference(frame_id, frame)
		t1 = time.time()

		# Вместо прямого вызова update_frame (это опасно из другого потока), 
		# мы просто сохраняем результаты в session_state.
		st.session_state['latest_frame'] = frame
		st.session_state['latest_res'] = res
		st.session_state['latest_inf_time'] = t1 - t0
		st.session_state['current_frame_id'] = frame_id
		
		# Задержка, которая не блокирует основной UI
		time.sleep(1.0 / fps)

	st.session_state['processing_complete'] = True

"""
if start_button and video:
	# Сохраняем видео во временный файл
	temp_video_path = tempfile.NamedTemporaryFile(
			delete=False #, suffix=".mp4"
	)
	temp_video_path.write(video.read())
	temp_video_path.close()

	# окошки
	col_left, col_right = st.columns([1.3, 1])	
	with col_left:
		frame_placeholder   = st.empty() # область для обновления кадра
	with col_right:
		metrics_placeholder = st.empty() # область для статистик
	progress = st.progress(0)   # полоса прогресса

	total_frames = 1000  # ЗАГЛУШКА
	start_time = time.time()

	# обработка по кадрово
	for frame_id, frame in generate_frames(temp_video_path.name):
		t0 = time.time()
		res = run_inference(frame_id, frame)
		t1 = time.time()
		
		# Обновление блоков
		update_frame(frame_placeholder, frame, frame_id, res)
		update_metrics(metrics_placeholder, res, t1 - t0)
	        
		progress.progress((frame_id + 1) / total_frames)
		
		# Задержка, чтобы не нагружать.
		time.sleep(1.0 / fps)

	total_time = time.time() - start_time
	st.success("Обработка завершена за {total_time:.1f} секунд!")
"""

if 'processing_running' not in st.session_state:
	st.session_state['processing_running'] = False
	st.session_state['processing_complete'] = False
	# Инициализируем другие переменные session_state

if start_button and video and not st.session_state['processing_running']:
	# Сохраняем видео во временный файл
	temp_video_path = tempfile.NamedTemporaryFile(
			delete=False #, suffix=".mp4"
	)
	temp_video_path.write(video.read())
	temp_video_path.close()
	total_frames = 1000
	
	# Запуск обработки в новом потоке при первом запуске
	thread = threading.Thread(
		target=process_video_in_background, 
		args=(temp_video_path.name, total_frames)
	)
	thread.daemon = True # Поток завершится при закрытии приложения
	thread.start()
	st.session_state['processing_running'] = True

if 'latest_frame' in st.session_state:
	# Здесь вызываются функции обновления UI в основном потоке Streamlit
	update_frame(
		frame_placeholder, 
		st.session_state['latest_frame'], 
		st.session_state['current_frame_id'], 
		st.session_state['latest_res']
	)
	update_metrics(
		metrics_placeholder, 
		st.session_state['latest_res'], 
		st.session_state['latest_inf_time']
	)
	
	progress_val = (st.session_state['current_frame_id'] + 1) / total_frames
	progress.progress(progress_val)
	
	if not st.session_state['processing_complete']:
		# ВАЖНО: Принудительный перезапуск Streamlit, чтобы UI обновился 
		# и показал последние данные из session_state
		st.rerun()

# =============================
#     ИСТОРИЯ СОБЫТИЙ
# =============================

# === История ===
if st.session_state.history:
	st.markdown("---")
	st.markdown("### История проверок")
	st.dataframe(st.session_state.history[-10:][::-1], use_container_width=True, hide_index=True)

# =============================
#     ПОДВАЛ СТРАНИЦЫ
# =============================

# === Футер ===
st.markdown("---")
st.markdown(
	"<p style='text-align: center; color: grey;'>"
	"CV-10 • ИИ-контроль СИЗ в ИК-диапазоне • Работает без интернета"
	"</p>",
	unsafe_allow_html=True
)
