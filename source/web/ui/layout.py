import streamlit as st


# =============================
#      ЗАГОЛОВОК И ШАПКА
# =============================
def render_header():
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
#     ПОДВАЛ СТРАНИЦЫ
# =============================
# === Футер ===
def render_futer():
	st.markdown("---")
	st.markdown(
		"<p style='text-align: center; color: grey;'>"
		"CV-10 • ИИ-контроль СИЗ в ИК-диапазоне"  # • Работает без интернета
		"</p>",
		unsafe_allow_html=True
	)
