import datetime
from dataclasses import dataclass
from typing import List
import pandas as pd
import pymysql.cursors
import streamlit as st
from const import Constants
from dbutils.pooled_db import PooledDB

# Connection Pool
POOL = PooledDB(pymysql, maxconnections=150, **Constants.DB_CONFIG)

def get_connection():
    return POOL.connection()

def init_db():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Constants.DB_CONFIG['db']}")

            cursor.execute(f"USE {Constants.DB_CONFIG['db']}")

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS submitlog (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    username VARCHAR(255) NOT NULL,
                    public_score DOUBLE NOT NULL,
                    private_score DOUBLE NOT NULL
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE  IF NOT EXISTS team (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    icon MEDIUMBLOB NOT NULL
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS discussion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    username VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content MEDIUMBLOB NOT NULL
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS likes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    username VARCHAR(255) NOT NULL,
                    discussion_id INT NOT NULL
                );
                """
            )

            connection.commit()

    finally:
        connection.close()

def get_submit() -> pd.DataFrame:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM submitlog"
            cursor.execute(sql)
            result = cursor.fetchall()

            df = pd.DataFrame(
                result,
                columns=[
                    "id",
                    "post_date",
                    "username",
                    "public_score",
                    "private_score",
                ],
            )
            df["post_date"] = pd.to_datetime(df["post_date"])
            return df

    finally:
        connection.close()


def add_submit(username: str, public_score: float, private_score: float):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO submitlog (username, public_score, private_score) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, public_score, private_score))
            connection.commit()

    finally:
        connection.close()


def get_team(team_id: int) -> pd.DataFrame:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM team WHERE id = %s"
            cursor.execute(sql, team_id)
            result = cursor.fetchone()

            return result

    finally:
        connection.close()


def get_teamicon(team_id: int) -> bytes:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT icon FROM team WHERE id = %s"
            cursor.execute(sql, team_id)
            result = cursor.fetchone()

            return result["icon"]

    finally:
        connection.close()


def add_team(team_id: int, name: str, icon_binaries: bytes, skip: bool = False):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM team WHERE id = %s", (team_id,))
            if cursor.fetchone()["COUNT(*)"] == 0:
                sql = "INSERT INTO team (id, name, icon) VALUES (%s, %s, %s)"
                cursor.execute(sql, (team_id, name, icon_binaries))
            else:
                if not skip:
                    update_teamname(team_id, name)
                    update_teamicon(team_id, icon_binaries)

            connection.commit()
    finally:
        connection.close()


def update_teamname(team_id: int, name: str):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE team SET name = %s WHERE id = %s"
            cursor.execute(sql, (name, team_id))
            connection.commit()

    finally:
        connection.close()


def update_teamicon(team_id: int, icon_binaries: bytes):
    connection = get_connection()
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


def get_discussions() -> List[Discussion]:
    connection = get_connection()

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
    connection = get_connection()

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
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM likes WHERE discussion_id = %s"
            cursor.execute(sql, discussion_id)
            result = cursor.fetchone()

            return result["COUNT(*)"]

    finally:
        connection.close()


def put_favorite(username: str, discussion_id: int):
    connection = get_connection()

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
    connection = get_connection()

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


def get_all_teamname() -> List[str]:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM team"
            cursor.execute(sql)
            result = cursor.fetchall()

            return [row["name"] for row in result]

    finally:
        connection.close()
