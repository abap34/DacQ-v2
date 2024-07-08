import streamlit as st

from db import init_db
from team import setup_team
from user import get_all_user, get_username
from utils import load_env


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
        st.toast(
            f"ユーザ {username} としてログインしました。", 
            icon="✅"
        )

    return attendee


def setup():
    st.set_page_config(
        page_title="DacQ",
        page_icon="🦆",
        layout="wide",
    )

    init_db()
    setup_team(skip=True)
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

