import streamlit as st
from utils import load_rules

@st.cache_data()
def select_rules(env):
    st.write("Rules")
    rules = load_rules()
    st.markdown(rules, unsafe_allow_html=True)
