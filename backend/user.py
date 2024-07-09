import os

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers

from team import get_team_setting


def get_username():
    headers = _get_websocket_headers()
    user = headers.get("X-Forwarded-User")
    # local mode
    dev = os.getenv("DEV")
    if dev:
        if user is None:
            return "abap34"
    else:
        if user is None:
            st.error("Login required")
            st.stop()

    return user


def get_all_user() -> np.ndarray:
    team_setting = get_team_setting()

    all_user = pd.concat(
        [team_setting["user1"], team_setting["user2"], team_setting["user3"]],
        ignore_index=True,
    )

    return all_user.values
