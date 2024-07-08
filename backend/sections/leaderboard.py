import streamlit as st
from utils import get_current_phase, to_imagebase64, to_ranking
from db import get_submit

def select_leaderboard(env):
    current_phase = get_current_phase()
    submit = get_submit()
    ranking = to_ranking(submit, phase=current_phase)

    # ranking の icon を base64 に変換
    ranking["icon"] = ranking["icon"].apply(to_imagebase64)

    st.write("Ranking")
    st.dataframe(
        ranking,
        hide_index=True,
        column_config={
            "rank": {},
            "icon": st.column_config.ImageColumn(label="", width=50),
            "username": {},
            "score": st.column_config.NumberColumn(format="%.5f"),
            "submitcount": {},
            "lastsubmit": {},
        },
        use_container_width=True,
    )
