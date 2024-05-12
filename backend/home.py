import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image
import io

from score import validate, score, ValidateState
from db import get_submit, add_submit, update_teamicon, update_teamname
from const import Constants
from utils import (
    to_ranking,
    get_score_progress,
    get_sns_message,
    load_env,
    name_to_icon_url,
)
from team import setup_team, get_members


def select_leaderboard(env):
    submit = get_submit()
    ranking = to_ranking(submit)

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
    all_user = submit["username"].unique()
    user = st.selectbox("Select user", all_user)

    st.line_chart(get_score_progress(submit, user)["progress"])


def select_rules(env):
    st.write("Rules")
    with open("static/rules.md", "r") as f:
        rules = f.read()

    st.markdown(rules)


def select_submit(env):
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        validate_state = validate(df)
        if validate_state != 0:
            st.warning("Invalid file: " + ValidateState.warning_message(validate_state))
        else:
            label = pd.read_csv(Constants.LABEL_PATH)
            score_value = score(
                label[Constants.LABEL_COL].values, df[Constants.PRED_COL].values
            )

            # ベストスコアかどうかを判定
            # if not is_best_score(submit, score_value):
            # ベストスコアページに遷移

            # db に反映
            add_submit(env["username"], score_value, score_value)


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

    file_data = env["teamicon"]

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        # 128x128 にリサイズ
        image = Image.open(uploaded_file)
        image.thumbnail((128, 128))
        byte_io = io.BytesIO()
        image.save(byte_io, format="PNG")
        file_data = byte_io.getvalue()

    # チーム設定ボタン
    if st.button("Save"):
        st.write("Save your team setting.")
        st.write("New Team Name: " + team_name)
        st.write("New Team Icon: ")
        st.image(file_data, caption="New Icon")

        update_teamicon(env["teamid"], file_data)
        update_teamname(env["teamid"], team_name)

        # load_env.clear_cache()


def main():
    env = load_env()

    st.set_page_config(
        page_title="DacQ",
        page_icon="🦆",
        layout="wide",
    )

    st.markdown(
        "### 開催中のコンテスト:",
    )

    st.header(
        """
        # 寿司食べ犬すいコンテスト

        """,
        anchor="top",
        divider="orange",
    )

    selected = option_menu(
        None,
        ["LeaderBoard", "Submit", "Rules", "Score Log", "Team Setting"],
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
        "static/icon_svg.svg",
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
        f"https://q.trap.jp/share-target?text={get_sns_message(get_submit(), env['username'])}",
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


def setup():
    st.session_state["has_run_setup"] = True

    setup_team(
        # TODO: リリース時には False
        allow_duplicated=True
    )


if __name__ == "__main__":

    if "has_run_setup" not in st.session_state:
        setup()

    main()
