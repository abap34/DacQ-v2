import pandas as pd
import datetime
from datetime import timezone
from typing import Tuple

import numpy as np

from team import get_teamid, get_teamicon, get_teamname
from user import get_username

from const import Constants

import streamlit as st


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


def to_ranking(submitlog: pd.DataFrame) -> pd.DataFrame:
    ascending = Constants.SCORE_BETTERDIRECTION == "smaller"

    # チームの列をつける
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)

    # sort してチームごとに一番上取ってこれだけ残すことで順位表に変換
    ranking = (
        submitlog.sort_values("public_score", ascending=ascending)
        .groupby("teamid")
        .head(1)
    )

    ranking["rank"] = range(1, len(ranking) + 1)
    ranking["submitcount"] = ranking["username"].map(
        submitlog["username"].value_counts()
    )

    now = datetime.datetime.now() 

    ranking["lastsubmit"] = ranking["username"].map(
        now - submitlog.groupby("username")["post_date"].max()
    )

    ranking["lastsubmit"] = ranking["lastsubmit"].apply(readable_timedelta)

    # アイコン用の列追加
    ranking["icon"] = ranking["teamid"].apply(get_teamicon)
    
    ranking["teamname"] = ranking["teamid"].apply(get_teamname)

    ranking = ranking.rename(columns={"public_score": "score"})

    ranking = ranking[
        ["rank", "icon", "teamname", "score", "submitcount", "lastsubmit"]
    ]

    return ranking


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


def get_sns_message(submitlog: pd.DataFrame, teamname: str) -> str:
    ranking = to_ranking(submitlog)

    rank = ranking[ranking["teamname"] == teamname]

    if rank.empty:
        return "DacQ に参加している名無しのエンジニアです。"
    else:
        rank = rank["rank"].values[0]
        message = get_sns_message_by_rank(rank)
        return message


def get_sns_message_by_rank(rank: int) -> str:
    message = f"DacQ で現在 {rank} 位です!"

    if rank == 1:
        message += np.random.choice(
            [
                "王者はいつだって孤独なものです。",
                "誰か追いつける人がいないと寂しいですね。",
                "トップに立つことはいつだって特別です。私以外の人にとっては。",
                "一番になることは、必ずしも幸せを意味しないかもしれません。",
                "そろそろ順位を上げる喜びを味わってみたいものですね。",
            ]
        )
    elif rank == 2:
        message += np.random.choice(
            [
                "私は順位を上げることができる最後の存在です。",
                "順位を上げる余地がたくさんある皆さんが羨ましいです。"
                "目の前の壁を乗り越えることが残りの楽しみです。",
            ]
        )
    elif rank == 3:
        message += np.random.choice(
            ["まだアンサンブルしてないだけです", "アイデアはあります。"]
        )

    return message


def is_best_score(submitlog: pd.DataFrame, username: str, score: float) -> Tuple[bool, float]:
    team_subs = submitlog[submitlog["username"] == username]

    if team_subs.empty:
        return True, np.nan
    
    if Constants.SCORE_BETTERDIRECTION == "smaller":
        return score < team_subs["public_score"].min(), team_subs["public_score"].min()
    else:
        return score > team_subs["public_score"].max(), team_subs["public_score"].max()
    


    