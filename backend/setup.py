import streamlit as st
from db import init_db
from team import setup_team
from utils import load_env

def setup():
    st.set_page_config(
        page_title="DacQ",
        page_icon="🦆",
        layout="wide",
    )

    init_db()
    setup_team(skip=True)
    st.session_state["env"] = load_env()
    st.session_state["has_run_setup"] = True
