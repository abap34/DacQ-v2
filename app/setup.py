import os

import streamlit as st
from db import init_db
from streamlit_oauth import OAuth2Component
from team import setup_team
from user import get_all_user, get_username, is_login, login
from utils import load_env

def check_devmode():
    if os.environ.get("DEV"):
        st.session_state["DEV"] = True

def is_attendee():
    username = get_username()
    all_user = get_all_user()
    attendee = username in all_user
    if not attendee:
        st.toast(
            "ゲストユーザとしてログインします。",
            icon="ℹ️",
        )
    else:
        st.toast(f"ユーザ {username} としてログインしました。", icon="✅")

    return attendee


def setup():
    init_db()
    check_devmode()
    setup_team(skip=True)

    st.set_page_config(
        page_title="DacQ - home",
        page_icon="🦆",
        layout="wide",
    )

    if not is_login():
        login()    
    
    attendee = is_attendee()

    if attendee:
        st.session_state["env"] = load_env()
    else:
        st.session_state["env"] = {
            "username": "Guest",
            "teamname": "Guest",
        }

    st.session_state["attendee"] = attendee
    st.session_state["has_run_setup"] = True
