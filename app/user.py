import base64
import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_oauth import OAuth2Component
from team import get_team_setting


def get_payload(token: str) -> dict:
    payload = token.split(".")[1]
    payload += "=" * ((4 - len(payload) % 4) % 4)
    return json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))

def get_user_name(token: str) -> str:
    return get_payload(token)["name"]


AUTHORIZE_URL = os.environ["AUTHORIZE_URL"]
TOKEN_URL = os.environ["TOKEN_URL"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint=AUTHORIZE_URL,
    token_endpoint=TOKEN_URL,
)


def is_login():
    if os.environ.get("DEV"):
        return True
    
    if "token" in st.session_state:
        return True
    else:
        return False


def login():
    result = oauth2.authorize_button(
        "Authorize", REDIRECT_URI, "openid", key="trap", pkce="S256"
    )

    if result and "token" in result:
        st.session_state["token"] = result["token"]
        token_str = str(result.get("token"))
        username = get_user_name(token_str)
        st.session_state["username"] = username
        st.toast(f"Login finished! Welcome, {username}!", icon="✅")
        st.rerun()

    st.stop()

def get_username():
    if os.environ.get("DEV"):
        return "abap34"

    login = is_login()
    if not login:
        st.toast("Login required!", icon="⚠️")
        login()

    assert "token" in st.session_state

    return st.session_state["username"].lower()


def get_all_user() -> np.ndarray:
    team_setting = get_team_setting()

    # check user name is unique
    user_col = [col for col in team_setting.columns if col.startswith("user")]
    all_user = team_setting[user_col].melt()["value"].str.strip()
    all_user = all_user.dropna()



    return all_user.values
