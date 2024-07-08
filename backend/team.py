# base64
import io
from typing import List, Union

import pandas as pd
import streamlit as st
from PIL import Image

import db
from const import Constants
from db import add_team, get_team

def get_all_teamname() -> List[str]:
    return db.get_all_teamname()


# df が
# 1. id が unique
# 2. カラムが [id, user1, user2, user3] からなる
# 3. user1, user2, user3 が unique　かチェック
def validate_team(df: pd.DataFrame) -> bool:
    if df.columns.tolist().sort() != ["id", "user1", "user2", "user3"].sort():
        raise ValueError("Invalid column name! Please check the data.")

    all_user = pd.concat([df["user1"], df["user2"], df["user3"]], ignore_index=True)

    all_user = all_user.dropna()

    if len(all_user.unique()) != len(all_user):
        raise ValueError("Duplicate user name! Please check the data.")

    return True


# db にチームの初期データを追加
# デフォルトのチーム名は "team {i}"
# デフォルトのアイコンは static/default_icon.png
def setup_team(skip: bool = True):
    team_df = pd.read_csv(Constants.TEAM_PATH)
    validate_team(team_df)

    with open("static/default_icon.png", "rb") as f:
        default_icon = f.read()

    for i in range(len(team_df)):
        team_id = team_df["id"][i]
        name = f"team {i}"
        icon_binaries = default_icon

        add_team(team_id, name, icon_binaries, skip=skip)


@st.cache_data
def get_team_setting():
    return pd.read_csv(Constants.TEAM_PATH)


@st.cache_data
def get_teamid(username: str) -> Union[int, None]:
    team_df = get_team_setting()

    melted = team_df.melt(id_vars=["id"], value_vars=["user1", "user2", "user3"])

    team_id = melted[melted["value"] == username]["id"].values

    if len(team_id) == 0:
        # raise ValueError(f"User {username} is not in any team.")
        st.warning(f"User {username} is not in any team.")
        return None
    else:
        team_id = team_id[0]

    return team_id


def get_teamicon(team_id: int) -> Image:
    team_icon = db.get_teamicon(team_id)

    # read binary data
    team_icon = Image.open(io.BytesIO(team_icon))

    return team_icon


def get_teamname_from_username(usernames: str) -> str:
    team_id = get_teamid(usernames)

    return get_teamname(team_id)


def get_teamname(team_id: int) -> str:
    return get_team(team_id)["name"]


@st.cache_data
def get_members(team_id: int) -> List[str]:
    team_df = get_team_setting()

    team = team_df[team_df["id"] == team_id]

    return [
        team["user1"].values[0],
        team["user2"].values[0],
        team["user3"].values[0],
    ]


def get_team_submit(submitlog: pd.DataFrame, teamid: int) -> pd.DataFrame:
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)

    team_subs = submitlog[submitlog["teamid"] == teamid]

    team_subs = team_subs.sort_values("post_date")

    return team_subs
