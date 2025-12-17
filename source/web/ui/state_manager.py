# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# state_manager.py

import streamlit as st


# =============================
#      ИНИЦИАЛИЗАЦИЯ st.session_state
# =============================
#
# st.session_state - это оперативная память сеанса

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
