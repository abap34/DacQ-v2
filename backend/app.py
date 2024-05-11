import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


from score import validate, score, ValidateState
from db import get_submit, add_submit
from const import Constants
from utils import to_ranking, load_css, is_best_score


def main():
    st.set_page_config(
        page_title="DacQ",
        page_icon="📈",
        layout="wide",
    )

    st.markdown(
        load_css("style.css"),
        unsafe_allow_html=True,
    )

    selected = option_menu(
        None,
        ["LeaderBoard", "Submit", "Rules", "Score Log"],
        icons=["house", "cloud-upload", "list-task", "file-earmark-text"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    st.markdown(
        """
             <div class='title'> 現在の順位表 </div>
            """,
        unsafe_allow_html=True,
    )

    submit = get_submit()

    # 順位表
    if selected == "LeaderBoard":
        ranking = to_ranking(submit)
        st.write("Ranking")
        st.write(ranking)

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
        user_submit = submit[submit["username"] == user]
        user_score = user_submit["public_score"]
        st.line_chart(user_score)


if __name__ == "__main__":
    main()
