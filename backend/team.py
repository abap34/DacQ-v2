import pandas as pd
from PIL import Image

# base64
import io

from const import Constants
from db import add_team, get_team
import db


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
def setup_team(allow_duplicated: bool = False):
    team_df = pd.read_csv(Constants.TEAM_PATH)
    validate_team(team_df)

    with open("static/default_icon.png", "rb") as f:
        default_icon = f.read()

    for i in range(len(team_df)):
        team_id = team_df["id"][i]
        name = f"team {i}"
        icon_binaries = default_icon
        add_team(team_id, name, icon_binaries, allow_duplicated)


def get_teamid(username: str) -> int:
    team_df = pd.read_csv(Constants.TEAM_PATH)

    melted = team_df.melt(id_vars=["id"], value_vars=["user1", "user2", "user3"])

    team_id = melted[melted["value"] == username]["id"].values[0]

    return team_id


def get_teamicon(team_id: int) -> Image:

    team_icon = db.get_teamicon(team_id)

    # read binary data
    team_icon = Image.open(io.BytesIO(team_icon))

    return team_icon


def get_teamname(usernames: str) -> str:
    team_id = get_teamid(usernames)

    team_name = get_team(team_id)["name"]

    return team_name
