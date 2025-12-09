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
