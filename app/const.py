import datetime
import os
from typing import Literal

import numpy as np
import pymysql.cursors
from sklearn.metrics import accuracy_score
import pandas as pd

from zoneinfo import ZoneInfo

class Constants:
    # ラベル、提出ファイルのカラム名
    ID_COL: str = ""
    # ラベルのカラム名
    LABEL_COL: str = ""
    # 提出ファイルの予測データを格納しているカラム名
    PRED_COL: str = ""


    # 正解データのパス. `{LABEL_COL}`, `{LABEL_COL}` というカラムが必要
    LABEL_PATH: str = "static/.csv"

    # Pulic LB / Private LB の設定ファイル. 
    # `{ID_COL}`, `"setting"` というカラムが必要. `"setting` カラムには `"public"` か `"private"` が入っていて、それによって Public LB用のデータか Private LB用のデータかを判別する
    PUBLIC_PRIVATE_SETTING = "static/.csv"

    # チームの設定ファイル. `{ID_COL}`, `"user{1,2,3,...}` というカラムからなる.
    TEAM_PATH = "static/.csv"
    # 最終サブミットとして残せるファイル数
    PRIVATE_SUBMIT_COUNT = 0


    # DB の設定.
    DB_CONFIG = {
        "host": "",
        "port": 0,
        "user": "",
        "password": "",
        "db": "",
        "charset": "",
        "cursorclass": pymysql.cursors.DictCursor,
    }

    # スコアの並び順. "larger"だとスコアの値が大きい方が上位になり、"smaller"だとスコアの値が小さい方が上位になる
    SCORE_BETTERDIRECTION: Literal["smaller", "larger"] = ""


    # データセットの設定. Data タブに掲載される
    DATASETS = {
        "train": "",
        "test": "",
        "train_tiny": "",
        "test_tiny": "",
        "sample_submission": "",
    }

    # Public / Private の期間
    DATE = {
        "public_start": datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "public_end": datetime.datetime(2024, 1, 2, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "private_start": datetime.datetime(2024, 1, 3, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "private_end": datetime.datetime(2024, 1, 4, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
    }

    # スコアの計算方法
    @staticmethod
    def score(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
        return 0.0

    # 順位表に載せるプログレスバーのスケーリング方法
    @staticmethod
    def progress_scaler(scores: pd.Series) -> pd.Series:
        return scores
    
