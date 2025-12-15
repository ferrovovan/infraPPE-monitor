# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# layout.py
import streamlit as st


# =============================
#      ЗАГОЛОВОК И ШАПКА
# =============================
def render_header():
	# === Настройка страницы ===
	st.set_page_config(
		page_title="InfraPPE Monitor | AI-видеоконтроль экипировки",
		page_icon="hard-hat",  # Изменено на более тематический
		layout="wide",
		initial_sidebar_state="expanded"
	)

	# === Улучшенные стили ===
	st.markdown("""
	<style>
		.big-font {
			font-size: 42px !important;
			font-weight: 800 !important;
			color: #1E3A8A;
			font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
		}
		.risk-low {
			background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%);
			padding: 22px;
			border-radius: 14px;
			border-left: 8px solid #16A34A;
			box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
		}
		.risk-medium {
			background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
			padding: 22px;
			border-radius: 14px;
			border-left: 8px solid #D97706;
			box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
		}
		.risk-high {
			background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
			padding: 22px;
			border-radius: 14px;
			border-left: 8px solid #DC2626;
			box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
		}
		.header-box {
			background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 50%, #60A5FA 100%);
			padding: 30px 40px;
			border-radius: 18px;
			color: white;
			text-align: center;
			margin-bottom: 25px;
			box-shadow: 0 8px 25px rgba(30, 64, 175, 0.25);
			border: 1px solid rgba(255, 255, 255, 0.15);
			position: relative;
			overflow: hidden;
		}
		.header-box::before {
			content: '';
			position: absolute;
			top: -50%;
			left: -50%;
			width: 200%;
			height: 200%;
			background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
			background-size: 20px 20px;
			opacity: 0.3;
			z-index: 0;
		}
		.header-box h1 {
			font-size: 2.8rem;
			font-weight: 800;
			margin-bottom: 8px;
			position: relative;
			z-index: 1;
			text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
		}
		.header-box p {
			font-size: 1.2rem;
			opacity: 0.92;
			margin-top: 5px;
			position: relative;
			z-index: 1;
			font-weight: 300;
			letter-spacing: 0.5px;
		}
		.subtitle {
			color: #6B7280;
			font-size: 1.1rem;
			margin-top: -10px;
			margin-bottom: 25px;
			text-align: center;
			font-style: italic;
		}
		.st-emotion-cache-16idsys p {
			font-size: 1.05rem;
			line-height: 1.6;
		}
	</style>
	""", unsafe_allow_html=True)

	# === Оригинальная шапка ===
	header_html = """
	<div class="header-box">
		<h1>InfraPPE Monitor</h1>
		<p>Интеллектуальный контроль средств защиты в инфракрасном диапазоне</p>
	</div>
	"""
	st.markdown(header_html, unsafe_allow_html=True)


# =============================
#     ПОДВАЛ СТРАНИЦЫ
# =============================
# === Футер ===
def render_futer():
	st.markdown("---")
	st.markdown(
		"<p style='text-align: center; color: grey;'>"
		"Система инфракрасного мониторинга экипировки CV-10."
		" Автономная работа."
		#" Адаптировано для условий низкой видимости."
		"</p>",
		unsafe_allow_html=True
	)
