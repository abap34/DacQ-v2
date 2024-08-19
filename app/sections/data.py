import streamlit as st
from const import Constants

with open("static/data_description.md", "r") as f:
    data_description = f.read()


def select_data(_env):
    datasets = Constants.DATASETS
    st.write(data_description, unsafe_allow_html=True)
    
    st.write("### Download")
    
    for name, url in datasets.items():
        st.write(
            f"""
            ### {name}
            [Download {name}]({url})
            """
        )

