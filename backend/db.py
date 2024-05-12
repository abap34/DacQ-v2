from dataclasses import dataclass
import datetime
import pymysql.cursors
import pandas as pd
from PIL import Image
import io
from typing import List

import streamlit as st

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


def get_team(team_id: int) -> pd.DataFrame:
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM team WHERE id = %s"
            cursor.execute(sql, team_id)
            result = cursor.fetchone()

            return result

    finally:
        connection.close()


def get_teamicon(team_id: int) -> bytes:
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT icon FROM team WHERE id = %s"
            cursor.execute(sql, team_id)
            result = cursor.fetchone()

            return result["icon"]

    finally:
        connection.close()


def add_team(team_id: int, name: str, icon_binaries: bytes, allow_duplicated: bool):
    connection = pymysql.connect(**Constants.DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # IDが存在するかチェックするためのSQL文
            cursor.execute("SELECT COUNT(*) FROM team WHERE id = %s", (team_id,))
            if cursor.fetchone()["COUNT(*)"] == 0:
                # IDが存在しない場合は新規追加
                sql = "INSERT INTO team (id, name, icon) VALUES (%s, %s, %s)"
                cursor.execute(sql, (team_id, name, icon_binaries))
            else:
                if not allow_duplicated:
                    raise ValueError("ID already exists")

                # IDが存在する場合は更新
                sql = "UPDATE team SET name = %s, icon = %s WHERE id = %s"
                cursor.execute(sql, (name, icon_binaries, team_id))
            connection.commit()
    finally:
        connection.close()


def update_teamname(team_id: int, name: str):
    connection = pymysql.connect(**Constants.DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE team SET name = %s WHERE id = %s"
            cursor.execute(sql, (name, team_id))
            connection.commit()

    finally:
        connection.close()


def update_teamicon(team_id: int, icon_binaries: bytes):
    connection = pymysql.connect(**Constants.DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE team SET icon = %s WHERE id = %s"
            cursor.execute(sql, (icon_binaries, team_id))
            connection.commit()

    finally:
        connection.close()


@dataclass
class Discussion:
    id: int
    post_date: datetime.datetime
    title: str
    content: str
    username: str


# Discussionの列を取得
# 重いのでこれは cache する
def get_discussions() -> List[Discussion]:
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM discussion"
            cursor.execute(sql)
            result = cursor.fetchall()

            discussions = []
            for row in result:
                discussions.append(
                    Discussion(
                        id=row["id"],
                        post_date=row["post_date"],
                        title=row["title"],
                        content=row["content"],
                        username=row["username"],
                    )
                )

            return discussions

    finally:
        connection.close()


def add_discussion(title: str, content: bytes, username: str):
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = (
                "INSERT INTO discussion (title, content, username) VALUES (%s, %s, %s)"
            )
            cursor.execute(sql, (title, content, username))
            connection.commit()

    finally:
        connection.close()


def get_favoritecount(discussion_id: int) -> int:
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM likes WHERE discussion_id = %s"
            cursor.execute(sql, discussion_id)
            result = cursor.fetchone()

            return result["COUNT(*)"]

    finally:
        connection.close()


# いいねを追加. もし既にいいねしていたらそれを削除
def put_favorite(username: str, discussion_id: int):
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            if is_favorite(username, discussion_id):
                sql = "DELETE FROM likes WHERE username = %s AND discussion_id = %s"
            else:
                sql = "INSERT INTO likes (username, discussion_id) VALUES (%s, %s)"
            cursor.execute(sql, (username, discussion_id))
            connection.commit()

    finally:
        connection.close()


def is_favorite(username: str, discussion_id: int) -> bool:
    connection = pymysql.connect(**Constants.DB_CONFIG)

    try:
        with connection.cursor() as cursor:
            sql = (
                "SELECT COUNT(*) FROM likes WHERE username = %s AND discussion_id = %s"
            )
            cursor.execute(sql, (username, discussion_id))
            result = cursor.fetchone()

            return result["COUNT(*)"] > 0

    finally:
        connection.close()
