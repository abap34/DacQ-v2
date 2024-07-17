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
# 2. カラムが [id, use{num}...] からなるかチェック
# 3. NaN 除いて、 unique かチェック
def validate_team(df: pd.DataFrame) -> bool:
    # check id is exist
    if "id" not in df.columns:
        raise ValueError("No `id` column in team setting.")
    
    # check id is unique
    if len(df["id"].unique()) != len(df):
        raise ValueError("Duplicate team id! Please check the data.")
    
    # check columns
    for col in df.columns:
        if col == "id":
            continue
        if not col.startswith("user"):
            raise ValueError("Invalid column name! Please check the data.")
        
    # check user name is unique
    user_col = [col for col in df.columns if col.startswith("user")]
    all_user = df[user_col].melt()["value"].str.strip()
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


def get_team_setting():
    return pd.read_csv(Constants.TEAM_PATH)


def get_teamid(username: str) -> Union[int, None]:
    team_df = get_team_setting()
    user_col = [col for col in team_df.columns if col.startswith("user")]

    melted = team_df.melt(id_vars=["id"], value_vars=user_col, value_name="value")

    team_id = melted[melted["value"] == username]["id"].values

    if len(team_id) == 0:
        raise ValueError(f"User {username} is not in any team.")
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


def get_members(team_id: int) -> List[str]:
    team_df = get_team_setting()

    team = team_df[team_df["id"] == team_id]

    user_col = [col for col in team_df.columns if col.startswith("user")]

    members = team[user_col].melt()["value"].str.strip()
    
    return members


def get_team_df(team_ids: List[int]) -> pd.DataFrame:
    team_df = get_team_setting()
    
    # team_df["id"] を並べ替えて、team_ids と一緒になるようにする
    team_df = team_df.set_index("id").loc[team_ids].reset_index()

    return team_df


def get_team_submit(submitlog: pd.DataFrame, teamid: int) -> pd.DataFrame:
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)

    team_subs = submitlog[submitlog["teamid"] == teamid]

    team_subs = team_subs.sort_values("post_date")

    return team_subs
