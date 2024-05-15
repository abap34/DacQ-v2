import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers


@st.cache_data
def get_username():
    headers = _get_websocket_headers()
    user = headers.get("X-Forwarded-User")
    if user is None:
        raise ValueError("User not found")
    return user