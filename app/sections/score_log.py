import streamlit as st

from db import get_submit
from team import get_all_teamname
from utils import get_score_progress

def select_score_log(_env):
    submit = get_submit()
    all_team = get_all_teamname()
    team = st.selectbox("Select Team", all_team)
    st.line_chart(get_score_progress(submit, team)["progress"])
