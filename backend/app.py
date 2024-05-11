import streamlit as st

from utils import get_submit, to_ranking

def main():
    st.title("Hello, Streamlit!")

    submit = get_submit()



    # 全ての投稿
    st.write("All submits")
    st.write(submit)


    # 順位表作る
    ranking = to_ranking(submit)


    # ランキング
    st.write("Ranking")
    st.write(ranking)






if __name__ == "__main__":
    main()