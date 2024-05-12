from typing import Literal
import pymysql.cursors

class Constants:
    LABEL_PATH: str = 'data/label.csv'
    LABEL_COL: str = 'label'
    PRED_COL: str = 'pred'
    ID_COL: str = 'id'
    DB_CONFIG = {
        'host': 'mariadb',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'db': 'app_db',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    SCORE_BETTERDIRECTION: Literal['smaller', 'larger'] = 'smaller'

    SELCTED = ['LeaderBoard', 'Submit', 'Rules', 'Score Log']

    TEAM_PATH = 'data/team_setting.csv'