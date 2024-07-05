import os

import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers


def get_username():
    headers = _get_websocket_headers()
    user = headers.get("X-Forwarded-User")
    # local mode
    dev = os.getenv("DEV")
    if dev:
        if user is None:
            return "abap34"
    else:
        if user is None:
            st.error("Login required")
            st.stop()

    return user
