import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from score import validate, score, ValidateState
from db import get_submit, add_submit
from const import Constants
from utils import to_ranking, is_best_score, get_score_progress, get_sns_message
from user import get_username


def main():
    username = get_username()

    st.caption(f"Login as {username}")

    st.sidebar.image(
        "data/kaggle.png",
        width=150,
    )


    st.sidebar.markdown(
        f"""

        ## Welcome {username} to DacQ! 📈📊

        DacQ はデータ分析コンペプラットフォームです。

        - LeaderBoard: 現在の順位表を表示します。
        - Submit: 予測ファイルを提出できます。
        - Rules / Data: コンペのルールやデータのダウンロードができます。
        - Score Log: スコアの推移を表示します。
        
        """
    )

    selected = option_menu(
        None,
        ["LeaderBoard", "Submit", "Rules", "Score Log"],
        icons=["house", "cloud-upload", "list-task", "file-earmark-text"],
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


if __name__ == "__main__":
    st.set_page_config(
        page_title="DacQ",
        page_icon="📈",
        layout="wide",
    )

    st.header("🦆📈 DacQ 🦆")

    main()
