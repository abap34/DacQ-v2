import streamlit as st
from utils import get_current_phase, to_imagebase64, to_ranking, Phase
from db import get_submit


def select_leaderboard(env):
    current_phase = get_current_phase()
    if current_phase == Phase.before_public:
        st.write("## Competition has not started yet.")
        return
    
    if current_phase == Phase.after_public:
        st.write("## Public phase has ended. Please wait for the results.")
        return
    
    if current_phase == Phase.after_private:
        st.write("## Competition has ended.")
        return


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
