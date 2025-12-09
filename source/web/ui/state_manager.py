import streamlit as st


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
