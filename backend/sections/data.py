import streamlit as st
from const import Constants

def select_data(env):
    datasets = Constants.DATASETS
    st.write("## Data")
    for name, url in datasets.items():
        st.write(
            f"""
            ### {name}
            [Download {name}]({url})
            """
        )
