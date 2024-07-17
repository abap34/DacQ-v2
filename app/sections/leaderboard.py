import streamlit as st
from const import Constants
from db import get_submit
from utils import Phase, get_current_phase, to_imagebase64, to_ranking


def show_leaderboard(phase: Phase):
    def rank_styler(x):
        color = "white"
        styles = "font-weight: normal; font-size: 12px;"
        if x["rank"] == 1:
            styles = "font-weight: bold; font-size: 20px;"
            color = "rgba(255, 215, 0, 0.6)"
            return [f"background-color: {color}; {styles};" for _ in x]
        elif x["rank"] == 2:
            styles = "font-weight: bold; font-size: 20px;"
            color = "rgba(192, 192, 192, 0.6)"
            return [f"background-color: {color}; {styles};" for _ in x]
        elif x["rank"] == 3:
            styles = "font-weight: bold; font-size: 20px;"
            color = "rgba(205, 127, 50, 0.6)"
            return [f"background-color: {color}; {styles};" for _ in x]

        return ["" for _ in x]

    if phase == Phase.public:
        st.write("## Public Leaderboard")
        submit = get_submit()
        ranking = to_ranking(submit, phase=phase)

        progress_max = ranking["progress"].max()
        progress_min = ranking["progress"].min()
        n_row = ranking.shape[0]

        ranking["icon"] = ranking["icon"].apply(to_imagebase64)

        ranking_styled = ranking.style.apply(rank_styler, axis=1)

        user_cols = [col for col in ranking.columns if col.startswith("user")]

        column_config = {
            "rank": st.column_config.NumberColumn(width=50),
            "teamname": st.column_config.TextColumn(label="Team Name", width=300),
            "icon": st.column_config.ImageColumn(label="", width=150),
            "progress": st.column_config.ProgressColumn(
                width=75,
                min_value=progress_min - 0.01,
                max_value=progress_max,
                format=" ",
                label="",
            ),
            "score": st.column_config.NumberColumn(width=150, format="%.5f"),
            "submitcount": st.column_config.NumberColumn(width=50),
            "lastsubmit": {},
        }

        for col in user_cols:
            column_config[col] = st.column_config.ImageColumn(label="", width=50)

        st.dataframe(
            ranking_styled,
            hide_index=True,
            height=35 * n_row,
            column_config=column_config,
            use_container_width=True,
        )

    if phase == Phase.private:
        st.write("## Private Leaderboard")
        submit = get_submit()
        public_lb = to_ranking(submit, phase=Phase.public)
        public_lb["icon"] = public_lb["icon"].apply(to_imagebase64)
        private_lb = to_ranking(submit, phase=Phase.private)
        private_lb["icon"] = private_lb["icon"].apply(to_imagebase64)

        progress_max = private_lb["progress"].max()
        progress_min = private_lb["progress"].min()

        # shake を計算
        # 各 teamname に対して、public の rank - private の rank を計算
        shake = public_lb.merge(
            private_lb, on="teamname", suffixes=("_public", "_private")
        )
        shake = shake.set_index("teamname")
        private_lb["shake"] = private_lb["teamname"].apply(
            lambda x: shake.loc[x]["rank_public"] - shake.loc[x]["rank_private"]
        )

        def shake_icon(x):
            if x > 0:
                return str(x) + " ↑"
            if x < 0:
                return str(x) + " ↓"
            return ""

        private_lb["shake"] = private_lb["shake"].apply(shake_icon)

        def shake_styler(x):
            if "↑" in x:
                return "color: #32CD32"

            if "↓" in x:
                return "color: #FF6347"

            return ""

        private_lb_styled = private_lb.style.apply(rank_styler, axis=1).applymap(
            shake_styler, subset=["shake"]
        )

        column_config = {
            "rank": st.column_config.NumberColumn(width=50),
            "teamname": st.column_config.TextColumn(label="Team Name", width=300),
            "icon": st.column_config.ImageColumn(label="", width=150),
            "progress": st.column_config.ProgressColumn(
                width=75,
                min_value=progress_min - 0.01,
                max_value=progress_max,
                format=" ",
                label="",
            ),
            "score": st.column_config.NumberColumn(width=150, format="%.5f"),
            "submitcount": st.column_config.NumberColumn(width=50),
            "lastsubmit": {},
            "shake": {},
        }

        user_cols = [col for col in private_lb.columns if col.startswith("user")]

        for col in user_cols:
            column_config[col] = st.column_config.ImageColumn(label="", width=50)

        st.write("### Private Leaderboard")
        st.dataframe(
            private_lb_styled,
            hide_index=True,
            height=35 * 35,
            column_config=column_config,
            use_container_width=True,
        )


def select_leaderboard(_env):
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
