import datetime
import os
from typing import Literal

import numpy as np
import pymysql.cursors
from sklearn.metrics import accuracy_score
import pandas as pd
from scipy.stats import yeojohnson

from zoneinfo import ZoneInfo

class Constants:
    LABEL_PATH: str = "static/label.csv"
    LABEL_COL: str = "class"
    PRED_COL: str = "pred"
    ID_COL: str = "id"
    DB_CONFIG = {
        "host": os.getenv("NS_MARIADB_HOSTNAME", "mariadb"),
        "port": int(os.getenv("NS_MARIADB_PORT", 3306)),
        "user": os.getenv("NS_MARIADB_USER", "root"),
        "password": os.getenv("NS_MARIADB_PASSWORD", "password"),
        "db": os.getenv("NS_MARIADB_DATABASE", "app_db"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
    }

    SCORE_BETTERDIRECTION: Literal["smaller", "larger"] = "larger"

    TEAM_PATH = "static/team_setting.csv"
    PUBLIC_PRIVATE_SETTING = "static/public_private_setting.csv"
    PRIVATE_SUBMIT_COUNT = 2


    DATASETS = {
        "train": "https://abap34.com/trap_ml_lecture/public-data/train.csv",
        "test": "https://abap34.com/trap_ml_lecture/public-data/test.csv",
        "train_tiny": "https://abap34.com/trap_ml_lecture/public-data/train_tiny.csv",
        "test_tiny": "https://abap34.com/trap_ml_lecture/public-data/test_tiny.csv",
        "sample_submission": "https://abap34.com/trap_ml_lecture/public-data/sample_submission.csv",
    }

    DATE = {
        "public_start": datetime.datetime(2024, 7, 10, 18, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "public_end": datetime.datetime(2024, 7, 16, 23, 59, 59, tzinfo=ZoneInfo("Asia/Tokyo")),
        "private_start": datetime.datetime(2024, 7, 17, 17, 50, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        "private_end": datetime.datetime(2024, 9, 7, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    }

    @staticmethod
    def score(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
        return accuracy_score(y_true, y_pred)
    
    @staticmethod
    def progress_scaler(scores: pd.Series) -> np.ndarray:
        return scores
    
