import streamlit as st
from streamlit_option_menu import option_menu

from db import get_submit
from sections import data, leaderboard, rules, score_log, submit, team_setting
from setup import setup
from utils import get_sns_message


def main(session_state):
    env = session_state["env"]

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

    if session_state["attendee"]:
        option =  ["LeaderBoard", "Submit", "Data", "Rules", "Score Log", "Team Setting"]
    else:
        option = ["LeaderBoard", "Score Log"]


    selected = option_menu(
        None,
        option,
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

    # 順位表
    if selected == "LeaderBoard":
        leaderboard.select_leaderboard(env)

    elif selected == "Score Log":
        score_log.select_score_log(env)

    # ゲストユーザはここまで読める ここで return

    if not session_state["attendee"]:
        st.warning("ゲストとしてログインしています。順位表の閲覧のみが可能でサブミットなどはできません。間違いと思われる場合は運営にお問い合わせください。")
        return

    if selected == "Submit":
        submit.select_submit(env)

    elif selected == "Rules":
        rules.select_rules(env)


    elif selected == "Team Setting":
        team_setting.select_team_setting(env)

    elif selected == "Data":
        data.select_data(env)

    st.sidebar.link_button(
        "traQ に現在の順位を投稿する",
        f"https://q.trap.jp/share-target?text={get_sns_message(get_submit(), env['teamname'])}",
    )


if __name__ == "__main__":
    if "has_run_setup" not in st.session_state:
        setup()

    main(st.session_state)
