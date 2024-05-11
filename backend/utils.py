
import pandas as pd
import datetime
from datetime import timezone

from const import Constants

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
    ascending = (Constants.SCORE_BETTERDIRECTION == 'smaller')

    ranking = df.sort_values('public_score', ascending=ascending).groupby('username').head(1)

    ranking['rank'] = range(1, len(ranking) + 1)
    ranking['submitcount'] = ranking['username'].map(df['username'].value_counts())
    
    # tz/tokyo に合わせる
    now = datetime.datetime.now() + datetime.timedelta(hours=9)

    ranking['lastsubmit'] = ranking['username'].map(now - df.groupby('username')['post_date'].max())

    ranking['lastsubmit'] = ranking['lastsubmit'].apply(readable_timedelta)

    ranking = ranking[['rank', 'username', 'public_score', 'submitcount', 'lastsubmit']]
    return ranking

def is_best_score(df: pd.DataFrame, score: float) -> bool:
    if df.empty:
        return True
    if Constants.SCORE_BETTERDIRECTION == 'smaller':
        return score < df['public_score'].min()
    else:
        return score > df['public_score'].max()


def load_css(path: str) -> str:
    with open(path) as f:
        css = f.read()
    return f"<style>{css}</style>"

