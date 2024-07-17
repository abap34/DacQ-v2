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
    ID_COL: str = "id"
    # ラベルのカラム名
    LABEL_COL: str = "class"
    # 提出ファイルの予測データを格納しているカラム名
    PRED_COL: str = "pred"


    # 正解データのパス. `{LABEL_COL}`, `{LABEL_COL}` というカラムが必要
    LABEL_PATH: str = "static/label.csv"

    # Pulic LB / Private LB の設定ファイル. 
    # `{ID_COL}`, `"setting"` というカラムが必要. `"setting` カラムには `"public"` か `"private"` が入っていて、それによって Public LB用のデータか Private LB用のデータかを判別する
    PUBLIC_PRIVATE_SETTING = "static/public_private_setting.csv"

    # チームの設定ファイル. `{ID_COL}`, `"user{1,2,3,...}` というカラムからなる.
    TEAM_PATH = "static/team_setting.csv"
    # 最終サブミットとして残せるファイル数
    PRIVATE_SUBMIT_COUNT = 2


    # DB の設定.
    DB_CONFIG = {
        "host": os.getenv("NS_MARIADB_HOSTNAME", "mariadb"),
        "port": int(os.getenv("NS_MARIADB_PORT", 3306)),
        "user": os.getenv("NS_MARIADB_USER", "root"),
        "password": os.getenv("NS_MARIADB_PASSWORD", "password"),
        "db": os.getenv("NS_MARIADB_DATABASE", "app_db"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
    }

    # スコアの並び順. "larger"だとスコアの値が大きい方が上位になり、"smaller"だとスコアの値が小さい方が上位になる
    SCORE_BETTERDIRECTION: Literal["smaller", "larger"] = "larger"


    # データセットの設定. Data タブに掲載される
    DATASETS = {
        "train": "https://abap34.com/trap_ml_lecture/public-data/train.csv",
        "test": "https://abap34.com/trap_ml_lecture/public-data/test.csv",
        "train_tiny": "https://abap34.com/trap_ml_lecture/public-data/train_tiny.csv",
        "test_tiny": "https://abap34.com/trap_ml_lecture/public-data/test_tiny.csv",
        "sample_submission": "https://abap34.com/trap_ml_lecture/public-data/sample_submission.csv",
    }

    # Public / Private の期間
    DATE = {
        "public_start": datetime.datetime(2024, 7, 10, 18, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "public_end": datetime.datetime(2024, 7, 16, 23, 59, 59, tzinfo=ZoneInfo("Asia/Tokyo")),
        "private_start": datetime.datetime(2024, 7, 17, 17, 50, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "private_end": datetime.datetime(2024, 9, 7, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    }

    # スコアの計算方法
    @staticmethod
    def score(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
        return accuracy_score(y_true, y_pred)

    # 順位表に載せるプログレスバーのスケーリング方法
    @staticmethod
    def progress_scaler(scores: pd.Series) -> pd.Series:
        return scores
    
