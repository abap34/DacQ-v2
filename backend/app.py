import streamlit as st
import pandas as pd

st.title("Hello World!")

df = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [10, 20, 30, 40]
})  

st.write(df)


import pymysql.cursors

import pymysql

def fetch_data_to_dataframe():
    # データベース設定
    config = {
        'host': 'mariadb',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'db': 'app_db',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    # データベースに接続
    connection = pymysql.connect(**config)
    
    try:
        with connection.cursor() as cursor:
            # テーブルの内容を取得
            sql = "SELECT * FROM posts"
            cursor.execute(sql)
            result = cursor.fetchall()
            
            # 結果をDataFrameに変換
            df = pd.DataFrame(result)
            return df
    
    finally:
        # データベース接続を閉じる
        connection.close()



df = fetch_data_to_dataframe()

st.write("データベースから取得したデータ:")
st.write(df)