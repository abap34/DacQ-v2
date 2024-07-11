import streamlit as st
from utils import load_rules

def select_rules(_env):
    st.write("Rules")
    rules = load_rules()
    st.markdown(rules, unsafe_allow_html=True)
