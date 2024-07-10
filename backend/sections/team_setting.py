import streamlit as st
import pandas as pd
from PIL import Image
import io
from db import update_teamicon, update_teamname
from team import get_members
from utils import name_to_icon_url

def select_team_setting(env):
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
                "icon": st.column_config.ImageColumn(label="", width=50),
                "username": {"width": 200},
            },
        )

    team_name = st.text_input("Enter your team name", env["teamname"], max_chars=32)
    uploaded_file = st.file_uploader(
        "Choose a image file (will be resized to 128x128)", type=["png", "jpg"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        image = Image.open(uploaded_file)
        image = image.thumbnail((128, 128))
        byte_io = io.BytesIO()
        image.save(byte_io, format="PNG")
        file_data = byte_io.getvalue()
    else:
        byte_io = io.BytesIO()
        env["teamicon"].save(byte_io, format="PNG")
        file_data = byte_io.getvalue()

    if st.button("Save"):
        try:
            update_teamname(env["teamid"], team_name)
            update_teamicon(env["teamid"], file_data)
        except Exception as e:
            st.toast(f"Oops! Something went wrong: {e}", icon="💥")

        st.toast("Saved!", icon="👍")
