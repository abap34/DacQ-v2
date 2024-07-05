import base64
import io

import numpy as np
import pandas as pd
import requests
import streamlit as st
import yaml
from const import Constants
from db import add_submit, get_submit, init_db, update_teamicon, update_teamname
from PIL import Image
from score import ValidateState, score, validate
from streamlit_extras.let_it_rain import rain
from streamlit_option_menu import option_menu
from team import get_all_team, get_members, get_team_submit, setup_team
from utils import (
    Phase,
    get_score_progress,
    get_sns_message,
    is_best_score,
    load_env,
    load_rules,
    name_to_icon_url,
    to_ranking,
)


def to_imagebase64(image: Image) -> str:
    byte_io = io.BytesIO()
    image.save(byte_io, format="PNG")
    return "data:image/png;base64," + base64.b64encode(byte_io.getvalue()).decode(
        "utf-8"
    )


def get_current_phase() -> Phase:
    now = pd.Timestamp.now()
    if now < Constants.DATE["public_start"]:
        return Phase.before_public
    elif now < Constants.DATE["public_end"]:
        return Phase.public
    elif now < Constants.DATE["private_start"]:
        return Phase.between
    elif now < Constants.DATE["private_end"]:
        return Phase.private
    else:
        return Phase.after_private


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
            "icon": st.column_config.ImageColumn(
                label="",
                width=50,
            ),
            "username": {},
            "score": st.column_config.NumberColumn(
                format="%.5f",
            ),
            "submitcount": {},
            "lastsubmit": {},
        },
        use_container_width=True,
    )


def select_score_log(env):
    submit = get_submit()

    all_team = get_all_team(submit)
    team = st.selectbox("Select Team", all_team)

    st.line_chart(get_score_progress(submit, team)["progress"])


def select_rules(env):
    st.write("Rules")
    rules = load_rules()
    st.markdown(rules)


def select_submit(env):
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
                public_private_setting = pd.read_csv(Constants.PUBLIC_PRIVATE_SETTING)
                public_mask = public_private_setting["setting"] == "public"
                private_mask = public_private_setting["setting"] == "private"
                assert np.logical_or(public_mask, private_mask).all()

                public_score = score(
                    label[Constants.LABEL_COL].values[public_mask],
                    df[Constants.PRED_COL].values[public_mask],
                )

                private_score = score(
                    label[Constants.LABEL_COL].values[private_mask],
                    df[Constants.PRED_COL].values[private_mask],
                )

                is_best, prev_best = is_best_score(submit, username, public_score)

                # ベストスコアかどうかを判定
                if not is_best:
                    st.toast("Not the best score... Keep trying!", icon="😢")
                else:
                    # お祝い
                    rain(
                        emoji="🎉",
                        animation_length=1,
                        falling_speed=2,
                    )

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

    st.button(
        "Submit !",
        on_click=_add_submit,
        args=(env["username"],),
        type="primary",
    )

    # 自分たちのサブミット一覧を見る
    team_subs = get_team_submit(submit, env["teamid"])

    st.write("Team's Submit")
    st.dataframe(
        team_subs[["username", "public_score", "post_date"]],
        hide_index=True,
        column_config={
            "username": {},
            "public_score": st.column_config.NumberColumn(
                format="%.5f",
            ),
            "post_date": {},
        },
        use_container_width=True,
    )


def select_team_setting(env):
    # チーム名設定
    st.write("## Team Setting")

    # 左右分割
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Team Name: " + env["teamname"])
        st.image(env["teamicon"], caption="Current Icon")
    with col2:
        st.write("### Members")
        members = get_members(env["teamid"])
        members_df = pd.DataFrame(members, columns=["username"])
        members_df["icon"] = members_df["username"].apply(name_to_icon_url)
        st.dataframe(
            members_df[["icon", "username"]],
            hide_index=True,
            column_config={
                "icon": st.column_config.ImageColumn(
                    label="",
                    width=50,
                ),
                "username": {
                    "width": 200,
                },
            },
        )

    # チーム名入力フォーム
    team_name = st.text_input("Enter your team name", env["teamname"], max_chars=32)
    # チームアイコン画像アップロード
    uploaded_file = st.file_uploader(
        "Choose a image file (will be resized to 128x128)", type=["png", "jpg"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        # 128x128 にリサイズ
        image = Image.open(uploaded_file)
        image.thumbnail((128, 128))
        byte_io = io.BytesIO()
        image.save(byte_io, format="PNG")
        file_data = byte_io.getvalue()
    else:
        byte_io = io.BytesIO()
        env["teamicon"].save(byte_io, format="PNG")
        file_data = byte_io.getvalue()

    # チーム設定ボタン
    if st.button("Save"):
        update_teamicon(env["teamid"], file_data)
        update_teamname(env["teamid"], team_name)


def data(env):
    datasets = Constants.DATASETS

    st.write("## Data")

    for name, url in datasets.items():
        # url に飛ぶ
        st.write(
            f"""

        ### {name}

        [Download {name}]({url})

        """
        )


def main(env):
    st.markdown(
        "### 開催中のコンペ: ",
    )

    st.header(
        """
        # 機械学習講習会 2024 記念 部内コンペ🦆📊

        """,
        anchor="top",
        divider="orange",
    )

    selected = option_menu(
        None,
        ["LeaderBoard", "Submit", "Data", "Rules", "Score Log", "Team Setting"],
        icons=["house", "cloud-upload", "list-task", "file-earmark-text", "people"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    st.caption(f"Login as {env['username']}")
    st.caption(f"Team: {env['teamname']}")

    st.markdown(
        """
    <style>
        section[data-testid="stSidebar"] {
            width: 120px !important; 
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.image(
        "static/icon.svg",
        width=180,
    )

    st.sidebar.markdown(
        f"""

        ## {env['username']}, Welcome to DacQ 🦆📊!

        DacQ はデータ分析コンペプラットフォームです。
        
        """
    )

    st.sidebar.link_button(
        "traQ に現在の順位を投稿する",
        f"https://q.trap.jp/share-target?text={get_sns_message(get_submit(), env['teamname'])}",
    )

    # 順位表
    if selected == "LeaderBoard":
        select_leaderboard(env)

    elif selected == "Submit":
        select_submit(env)

    elif selected == "Rules":
        select_rules(env)

    elif selected == "Score Log":
        select_score_log(env)

    elif selected == "Team Setting":
        select_team_setting(env)

    elif selected == "Data":
        data(env)


def setup():
    st.set_page_config(
        page_title="DacQ",
        page_icon="🦆",
        layout="wide",
    )

    init_db()

    setup_team(
        skip=True,
    )

    st.session_state["env"] = load_env()
    st.session_state["has_run_setup"] = True


if __name__ == "__main__":
    if "has_run_setup" not in st.session_state:
        setup()

    main(st.session_state["env"])
