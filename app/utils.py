import base64
import datetime
import io
from dataclasses import dataclass
from datetime import timezone
from typing import Tuple
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests
import streamlit as st
from const import Constants
from PIL import Image
from team import get_members, get_team_df, get_teamicon, get_teamid, get_teamname
from user import get_username


class Phase:
    before_public = 0
    public = 1
    between = 2
    private = 3
    after_private = 4


def get_current_phase() -> Phase:
    if st.session_state["DEV"] and "phase" in st.session_state:
        return st.session_state["phase"]

    now = pd.Timestamp.now(tz=ZoneInfo("Asia/Tokyo"))
    if now < Constants.DATE["public_start"]:
        return Phase.before_public
    elif now < Constants.DATE["public_end"]:
        return Phase.public
    elif now < Constants.DATE["private_start"]:
        return Phase.between
    elif now < Constants.DATE["private_end"]:
        return Phase.private
    else:
        return Phase.after_private


def load_env():
    username = get_username()
    teamid = get_teamid(username)
    teamname = get_teamname(teamid)
    teamicon = get_teamicon(teamid)

    return {
        "username": username,
        "teamname": teamname,
        "teamid": teamid,
        "teamicon": teamicon,
    }


def load_rules():
    with open("static/rules.md", "r") as f:
        rules = f.read()

    return rules


def name_to_icon_url(name: str) -> str:
    return f"https://q.trap.jp/api/v3/public/icon/{name}"


def readable_timedelta(td: datetime.timedelta) -> str:
    days = td // datetime.timedelta(days=1)
    hours = td // datetime.timedelta(hours=1) % 24
    minutes = td // datetime.timedelta(minutes=1) % 60
    seconds = td // datetime.timedelta(seconds=1) % 60

    if days < 1:
        if hours < 1:
            if minutes < 1:
                if seconds < 30:
                    return "just now"
                else:
                    return f"{seconds} seconds ago"
            else:
                return f"{minutes} minutes ago"
        else:
            return f"{hours} hours ago"
    else:

        return f"{days} days ago"


def to_imagebase64(image: Image) -> str:
    byte_io = io.BytesIO()
    image.save(byte_io, format="PNG")
    return "data:image/png;base64," + base64.b64encode(byte_io.getvalue()).decode(
        "utf-8"
    )


def to_ranking(submitlog: pd.DataFrame, phase: Phase = Phase.public) -> pd.DataFrame:
    if phase == Phase.before_public or phase == Phase.after_private:
        return pd.DataFrame(
            columns=["rank", "icon", "teamname", "score", "submitcount", "lastsubmit"]
        )

    sort_col = "public_score" if phase == Phase.public else "private_score"

    ascending = Constants.SCORE_BETTERDIRECTION == "smaller"

    # チームの列をつける
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)

    if phase == Phase.private:
        # 各チーム, 最新の `PRIVATE_SUBMIT_COUNT` だけ残す
        submitlog = (
            submitlog.sort_values("post_date")
            .groupby("teamid")
            .tail(Constants.PRIVATE_SUBMIT_COUNT)
        )

    # sort してチームごとに一番上取ってこれだけ残すことで順位表に変換
    ranking = (
        submitlog.sort_values(sort_col, ascending=ascending).groupby("teamid").head(1)
    )

    ranking["rank"] = range(1, len(ranking) + 1)
    ranking["submitcount"] = ranking["teamid"].map(submitlog["teamid"].value_counts())

    now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    lastsubmit_dates = submitlog.groupby("teamid")["post_date"].max()

    # post_date が JST で保存されているので、そのままに
    lastsubmit_dates = lastsubmit_dates.dt.tz_localize(ZoneInfo("Asia/Tokyo"))

    ranking["lastsubmit"] = ranking["teamid"].map(now - lastsubmit_dates)

    ranking["lastsubmit"] = ranking["lastsubmit"].apply(readable_timedelta)

    # アイコン用の列追加
    ranking["icon"] = ranking["teamid"].apply(get_teamicon)

    members_df = get_team_df(ranking["teamid"].values)

    ranking = pd.merge(ranking, members_df, left_on="teamid", right_on="id")

    user_col = [col for col in members_df.columns if col.startswith("user")]

    for col in user_col:
        ranking[col] = ranking[col].apply(name_to_icon_url)

    ranking["teamname"] = ranking["teamid"].apply(get_teamname)

    ranking = ranking.rename(columns={sort_col: "score"})

    ranking["progress"] = Constants.progress_scaler(ranking["score"])

    use_col = ["rank", "teamname", "icon"] + user_col + ["progress", "score", "submitcount", "lastsubmit"]

    return ranking[use_col]


def get_score_progress(submitlog: pd.DataFrame, teamname: str) -> pd.DataFrame:
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)
    submitlog["teamname"] = submitlog["teamid"].apply(get_teamname)
    team_subs = submitlog[submitlog["teamname"] == teamname]

    team_subs = team_subs.sort_values("post_date")

    if Constants.SCORE_BETTERDIRECTION == "smaller":
        team_subs["progress"] = team_subs["public_score"].cummin()
    else:
        team_subs["progress"] = team_subs["public_score"].cummax()

    team_subs = team_subs.set_index("post_date")

    return team_subs


def get_teamrank(submitlog: pd.DataFrame, teamname: str) -> int:
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)

    # これは常に public_score で ok
    ascending = Constants.SCORE_BETTERDIRECTION == "larger"
    sort_col = "public_score"
    # sort してチームごとに一番上取ってこれだけ残すことで順位表に変換
    ranking = (
        submitlog.sort_values(sort_col, ascending=ascending).groupby("teamid").head(1)
    )

    ranking["rank"] = range(1, len(ranking) + 1)

    return ranking[ranking["teamname"] == teamname]["rank"].values[0]


def is_best_score(
    submitlog: pd.DataFrame, username: str, score: float
) -> Tuple[bool, float]:
    team_subs = submitlog[submitlog["username"] == username]

    if team_subs.empty:
        return True, np.nan

    if Constants.SCORE_BETTERDIRECTION == "smaller":
        return score < team_subs["public_score"].min(), team_subs["public_score"].min()
    else:
        return score > team_subs["public_score"].max(), team_subs["public_score"].max()
