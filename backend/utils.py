import pandas as pd
import datetime
from datetime import timezone

import numpy as np

from team import get_teamid, get_teamicon, get_teamname
from user import get_username

from const import Constants


def load_env():
    username = get_username()
    teamname = get_teamname(username)
    teamid = get_teamid(username)
    teamicon = get_teamicon(teamid)

    return {
        "username": username,
        "teamname": teamname,
        "teamid": teamid,
        "teamicon": teamicon,
    }

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


def to_ranking(df: pd.DataFrame) -> pd.DataFrame:
    # ユーザの最高スコア順に並び替え. user ごとに uniqe にして最高スコアのみを取得
    ascending = Constants.SCORE_BETTERDIRECTION == "smaller"

    ranking = (
        df.sort_values("public_score", ascending=ascending).groupby("username").head(1)
    )

    ranking["rank"] = range(1, len(ranking) + 1)
    ranking["submitcount"] = ranking["username"].map(df["username"].value_counts())

    # tz/tokyo に合わせる
    now = datetime.datetime.now() + datetime.timedelta(hours=9)

    ranking["lastsubmit"] = ranking["username"].map(
        now - df.groupby("username")["post_date"].max()
    )

    ranking["lastsubmit"] = ranking["lastsubmit"].apply(readable_timedelta)

    # アイコン用の列追加
    ranking["icon"] = ranking["username"].apply(
        lambda name: f"https://q.trap.jp/api/v3/public/icon/{name}"
    )

    ranking = ranking.rename(columns={"public_score": "score"})

    ranking = ranking[
        ["rank", "icon", "username", "score", "submitcount", "lastsubmit"]
    ]

    return ranking



def get_score_progress(df: pd.DataFrame, username: str) -> pd.DataFrame:
    user_df = df[df["username"] == username]

    user_df = user_df.sort_values("post_date")

    if Constants.SCORE_BETTERDIRECTION == "smaller":
        user_df["progress"] = user_df["public_score"].cummin()
    else:
        user_df["progress"] = user_df["public_score"].cummax()

    user_df = user_df.set_index("post_date")

    return user_df


def get_sns_message(df: pd.DataFrame, username: str) -> str:
    rank = to_ranking(df)[username == df["username"]]

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
