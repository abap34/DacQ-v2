import pymysql.cursors
import pandas as pd
from const import Constants


def get_submit() -> pd.DataFrame:
    # データベースに接続
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM submitlog"
            cursor.execute(sql)
            result = cursor.fetchall()

            df = pd.DataFrame(result)
            return df

    finally:
        connection.close()


def add_submit(username: str, public_score: float, private_score: float):
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO submitlog (username, public_score, private_score) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, public_score, private_score))
            connection.commit()

    finally:
        connection.close()
