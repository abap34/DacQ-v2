import base64
import datetime
import io
from dataclasses import dataclass
from datetime import timezone
from typing import Tuple

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from const import Constants
from team import get_teamicon, get_teamid, get_teamname
from user import get_username


class Phase:
    before_public = 0
    public = 1
    between = 2
    private = 3
    after_private = 4


def get_current_phase() -> Phase:
    now = pd.Timestamp.now()
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


@st.cache_data
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
    if phase not in [Phase.public, Phase.private]:
        return pd.DataFrame(
            columns=["rank", "icon", "teamname", "score", "submitcount", "lastsubmit"]
        )

    sort_col = "public_score" if phase == Phase.public else "private_score"

    ascending = Constants.SCORE_BETTERDIRECTION == "smaller"

    # チームの列をつける
    submitlog["teamid"] = submitlog["username"].apply(get_teamid)

    # sort してチームごとに一番上取ってこれだけ残すことで順位表に変換
    ranking = (
        submitlog.sort_values(sort_col, ascending=ascending).groupby("teamid").head(1)
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

    ranking = ranking.rename(columns={sort_col: "score"})

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
                "そろそろ順位を上げる喜びを味わってみたいものですね。",
                "どこかのチームが抜いてくれないと退屈ですね。",
                "追いかける人がいないと、何か物足りなさを感じます。",
                "頂点に立つことは常に特別なことですが、それは私以外の人にとってです。",
                "次の挑戦者が現れるのを楽しみにしています。",
                "誰かが私を抜いてくれると刺激があっていいかもしれないですね。",
            ]
        )
    elif rank == 2:
        message += np.random.choice(
            [
                "私は順位を上げることができる最後の存在です。",
                "順位を上げる余地がたくさんある皆さんが羨ましいです。"
                "目の前の壁を乗り越えることが残りの楽しみです。",
                "あと一つ背中を追い越せば、ついに望んだその順位です。",
            ]
        )
    elif rank == 3:
        message += np.random.choice(
            ["まだアンサンブルしてないだけです", "アイデアはあります。"]
        )

    return message


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
