import datetime
import os
from typing import Literal

import pymysql.cursors


class Constants:
    LABEL_PATH: str = "static/label.csv"
    LABEL_COL: str = "label"
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

    SCORE_BETTERDIRECTION: Literal["smaller", "larger"] = "smaller"

    TEAM_PATH = "static/team_setting.csv"
    PUBLIC_PRIVATE_SETTING = "static/public_private_setting.csv"

    DATASETS = {
        "train": "https://abap34.com/trap_ml_lecture/train.csv",
        "test": "https://abap34.com/trap_ml_lecture/test.csv",
    }

    DATE = {
        "public_start": datetime.datetime(2024, 7, 10, 18, 0, 0),
        "public_end": datetime.datetime(2024, 7, 17, 0, 0, 0),
        "private_start": datetime.datetime(2024, 7, 27, 17, 45, 0),
        "private_end": datetime.datetime(2024, 9, 7, 0, 0, 0),
    }
