import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.let_it_rain import rain

from const import Constants
from db import add_submit, get_submit
from score import ValidateState, validate
from team import get_team_submit
from utils import Phase, get_current_phase, is_best_score
from score import public_and_private_score


def select_submit(env):
    phase = get_current_phase()
    if phase != Phase.public:
        if phase == Phase.before_public:
            st.warning("Competition has not started yet.")
        elif phase == Phase.between:
            st.warning("Public phase has ended. Please wait for the results.")
        elif phase == Phase.after_private:
            st.warning("Competition has ended.")
        return
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    submit = get_submit()

    def _add_submit(username):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            validate_state = validate(df)
            if validate_state != 0:
                st.warning(
                    "Invalid file: " + ValidateState.warning_message(validate_state)
                )
            else:
                label = pd.read_csv(Constants.LABEL_PATH)
                
                public_score, private_score = public_and_private_score(
                    label[Constants.LABEL_COL].values,
                    df[Constants.PRED_COL].values,
                    
                )

                is_best, prev_best = is_best_score(submit, username, public_score)

                # ベストスコアかどうかを判定
                if not is_best:
                    st.toast("Not the best score... Keep trying!", icon="😢")
                else:
                    # お祝い
                    rain(emoji="🎉", animation_length=1, falling_speed=2)
                    st.success("Congratulations! You got the best score!")

                    if np.isnan(prev_best):
                        st.metric(
                            label="Your First Score! Keep it up! 🦆",
                            value=f"{public_score:.5f}",
                        )
                    else:
                        st.metric(
                            label="Best Score Updated ! ⤴️",
                            value=f"{public_score:.5f}",
                            delta=f"{public_score - prev_best:.5f}",
                        )

                    st.link_button(
                        "スコア更新を traQ に共有する!",
                        f"https://q.trap.jp/share-target?text=最高スコアを更新しました！今のスコアは{public_score:.5f}です :nityaa_harsh:",
                    )

                add_submit(env["username"], public_score, private_score)

    st.button("Submit !", on_click=_add_submit, args=(env["username"],), type="primary")

    # 自分たちのサブミット一覧を見る
    team_subs = get_team_submit(submit, env["teamid"])

    st.write("Team's Submit")
    st.dataframe(
        team_subs[["username", "public_score", "post_date"]],
        hide_index=True,
        column_config={
            "username": {},
            "public_score": st.column_config.NumberColumn(format="%.5f"),
            "post_date": {},
        },
        use_container_width=True,
    )
