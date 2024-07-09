import streamlit as st

from db import get_submit
from utils import Phase, get_current_phase, to_imagebase64, to_ranking




def show_leaderboard(phase: Phase):
    if phase == Phase.public:
        st.write("## Public Leaderboard")
        submit = get_submit()
        ranking = to_ranking(submit, phase=phase)

        ranking["icon"] = ranking["icon"].apply(to_imagebase64)

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

    if phase == Phase.private:
        st.write("## Private Leaderboard")
        submit = get_submit()
        public_lb = to_ranking(submit, phase=Phase.public)
        public_lb["icon"] = public_lb["icon"].apply(to_imagebase64)
        private_lb = to_ranking(submit, phase=Phase.private)
        private_lb["icon"] = private_lb["icon"].apply(to_imagebase64)

        # shake を計算
        # 各 teamname に対して、public の rank - private の rank を計算
        shake = public_lb.merge(private_lb, on="teamname", suffixes=("_public", "_private"))
        shake = shake.set_index("teamname")
        private_lb["shake"] = private_lb["teamname"].apply(lambda x: shake.loc[x]["rank_public"] - shake.loc[x]["rank_private"])

        def shake_icon(x):
            if x > 0:
                return "⇧ " + str(x)
            if x < 0:
                return "⇩ " + str(x)
            return "⇨" + str(x)
        
        private_lb["shake"] = private_lb["shake"].apply(shake_icon)

        def shake_styler(x):
            if "⇧" in x:
                return "color: green"
            
            if "⇩" in x:
                return "color: lightcoral"
            
            return "color: blue"
        
        def rank_styler(x):
            if x == 1:
                return "background-color: gold ; color: black ; font-weight: bold"
            if x == 2:
                return "background-color: silver ; color: black ; font-weight: bold"
            if x == 3:
                return "color: chocolate ; font-weight: bold"
            return ""
        
        private_lb_styled = private_lb.style.applymap(rank_styler, subset=["rank"]).applymap(shake_styler, subset=["shake"])

        st.write("### Private Leaderboard")
        st.dataframe(
            private_lb_styled,
            hide_index=True,
            column_config={
                "rank": {},
                "icon": st.column_config.ImageColumn(label="", width=50),
                "username": {},
                "score": st.column_config.NumberColumn(format="%.5f"),
                "submitcount": {},
                "lastsubmit": {},
                "rank_public": {},
                "rank_private": {},
                "shake": {}
            },
            use_container_width=True,
        )

        

    

def select_leaderboard(env):
    current_phase = get_current_phase()
    if current_phase == Phase.before_public:
        st.warning("Competition has not started yet.")
        return

    if current_phase == Phase.between:
        st.warning("Public phase has ended. Please wait for the results.")
        return

    if current_phase == Phase.after_private:
        st.warning("Competition has ended.")
        return

    if current_phase == Phase.public:
        show_leaderboard(Phase.public)

    # private は両方出す
    if current_phase == Phase.private:
        show_leaderboard(Phase.private)
        show_leaderboard(Phase.public)

    return
