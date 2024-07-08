import streamlit as st
from db import get_submit
from team import get_all_team
from utils import get_score_progress

def select_score_log(env):
    submit = get_submit()
    all_team = get_all_team(submit)
    team = st.selectbox("Select Team", all_team)
    st.line_chart(get_score_progress(submit, team)["progress"])
