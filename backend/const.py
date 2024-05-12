from typing import Literal
import pymysql.cursors
import os

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
        "db": "app_db",
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
    }



    SCORE_BETTERDIRECTION: Literal["smaller", "larger"] = "smaller"

    TEAM_PATH = "static/team_setting.csv"
