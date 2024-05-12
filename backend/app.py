import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from PIL import Image

from score import validate, score, ValidateState
from db import get_submit, add_submit, update_teamicon, update_teamname
from team import get_teamname, setup_team, get_teamid, get_teamicon
from const import Constants
from utils import to_ranking, is_best_score, get_score_progress, get_sns_message
from user import get_username


def main():
    username = get_username()
    teamname = get_teamname(username)
    teamid = get_teamid(username)
    teamicon = get_teamicon(teamid)

    st.caption(f"Login as {username}")
    st.caption("Team: " + teamname)

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
        "data/icon_svg.svg",
        width=180,
    )

    st.sidebar.markdown(
        f"""

        ## {username}, Welcome to DacQ! 📈📊

        DacQ はデータ分析コンペプラットフォームです。

        - LeaderBoard: 現在の順位表を表示します。
        - Submit: 予測ファイルを提出できます。
        - Rules / Data: コンペのルール確認やデータのダウンロードができます。
        - Score Log: スコアの推移を表示します。
        
        """
    )

    selected = option_menu(
        None,
        ["LeaderBoard", "Submit", "Rules", "Score Log", "Team Setting"],
        icons=["house", "cloud-upload", "list-task", "file-earmark-text", "people"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    submit = get_submit()

    st.sidebar.link_button(
        "traQ に現在の順位を投稿する",
        f"https://q.trap.jp/share-target?text={get_sns_message(submit, username)}",
    )

    # 順位表
    if selected == "LeaderBoard":
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

    elif selected == "Submit":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

            validate_state = validate(df)
            if validate_state != 0:
                st.warning(
                    "Invalid file: " + ValidateState.warning_message(validate_state)
                )
            else:
                label = pd.read_csv(Constants.LABEL_PATH)
                score_value = score(
                    label[Constants.LABEL_COL].values, df[Constants.PRED_COL].values
                )

                # ベストスコアかどうかを判定
                # if not is_best_score(submit, score_value):
                # ベストスコアページに遷移

                # db に反映
                add_submit("abap34", score_value, score_value)

    elif selected == "Rules":
        st.write("Rules")
        st.markdown(
            """
            # 👀 Big Brother is watching you 🫵
            """
        )

    elif selected == "Score Log":
        all_user = submit["username"].unique()
        user = st.selectbox("Select user", all_user)

        st.line_chart(get_score_progress(submit, user)["progress"])

    elif selected == "Team Setting":
        # チーム名設定
        st.write("## Team Setting")
        st.write("Team Name: " + teamname)
        st.write("Team Icon Setting")
        st.image(teamicon, caption="Current Icon")

        # チーム名入力フォーム
        team_name = st.text_input("Enter your team name", teamname, max_chars=32)
        # チームアイコン画像アップロード
        uploaded_file = st.file_uploader(
            "Choose a image file (will be resized to 128x128)", type=["png", "jpg"]
        )

        file_data = teamicon

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
            # 128x128 にリサイズ
            image = Image.open(uploaded_file)
            image.thumbnail((128, 128))
            file_data = image.tobytes()

        # チーム設定ボタン
        if st.button("Save"):
            st.write("Save your team setting.")
            update_teamicon(teamid, file_data)
            update_teamname(teamid, team_name)


def setup():
    st.session_state["has_run_setup"] = True

    setup_team(
        # TODO: リリース時には False
        allow_duplicated=True
    )

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
        機械学習講習会ミニコンペ ~ メルカリコンペに挑戦してみよう！ ~
        """,
        anchor="top",
        divider="orange",
    )


if __name__ == "__main__":
    if "has_run_setup" not in st.session_state:
        setup()

    main()
