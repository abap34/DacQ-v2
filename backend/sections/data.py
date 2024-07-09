import streamlit as st
from const import Constants

HEAD = """

<style>
    h2 {
        border-bottom: 2px solid #eaecef;
        margin-bottom: 1em;

    }

    h3 {
        border-bottom: 1px solid #eaecef;
        margin-bottom: 1em;
    }
</style>

# Data

## Description

使用可能なデータは以下のとおりです。
このページ下のリンクからダウンロードできます。


- train.csv : 学習用データ
- test.csv : テスト用データ
- train-tiny.csv : 欠損値が含まれない学習用データのサブセット
- test-fillna.csv : 欠損値が全て0で埋められたテスト用データ
- sample_submission.csv : 提出用のサンプルファイル

### train.csv

学習用データです。

各レコードにはその通信の特徴量が含まれています。

以下のカラムからなります。

`class` が今回の目的変数です。

| カラム名 | データ型 | 欠損値 / ノイズ | 説明 | 目的変数 |
| --- | --- | --- | --- | --- |
| `id` | int | ❌ | データのID | - |
| `duration` | real | ⭕️ |  接続時間 (秒) | - |
| `protocol_type` | string |  ❌ | 通信プロトコル (`"tcp"`, `"udp"`, `"icmp"` のいずれか) | - |
| `service` | string | ❌ | 通信サービス (`"aol"`, "`auth`", `"bgp"` など) | - |
| `flag` | string | ❌ | 通信の状態 (`"OTH"`, `"REJ"`, `"RSTO"` など) | - |
| `src_bytes` | int | ⭕️ | 送信元バイト数 (src → dst) | - |
| `dst_bytes` | int | ⭕️ | 送信先バイト数 (dst → src) | - |
| `land` | int | ❌ | 送信元と送信先が同じかどうか (`1`: 同じ, `0`: 異なる) | - |
| `wrong_fragment` | int | ⭕️ | 不正なフラグメント数 |- |
| `urgent` | int | ⭕️ | urgent パケット数 |- |
| `hot` | int | ⭕️ | hot インジケータ数 |- |
| `num_failed_logins` | int | ⭕️ | ログイン失敗回数 |- |
| `logged_in` | int | ❌ | ログインに成功したか (`1`: 成功, `0`: 失敗) |- |
| `num_compromised` | int | ⭕️ | compromised 状態の回数 |- |
| `root_shell` | int | ⭕️ | ルートシェルを取得したか (`1`: 取得, `0`: 取得なし) |- |
| `su_attempted` | int | ⭕️ | su コマンドを施行した (`1`: 試行した, `0`: 試行なし) |- |
| `num_root` | int | ⭕️ | root アクセスの回数 |- |
| `num_file_creations` | int | ⭕️ | ファイル作成の試行回数 |- |
| `num_shells` | int | ⭕️ | シェルプロンプトの回数 |- |
| `num_access_files` | int | ⭕️ | アクセス制御ファイルの操作回数 |- |
| `num_outbound_cmds` | int | ⭕️ | アウトバウンドコマンドの回数 |- |
| `is_host_login` | int | ❌ | ログイン試行先が `root` または `admin` かどうか (`1`: `root` または `admin`, `0`: それ以外) |- |
| `is_guest_login` | int | ❌ | ログイン試行先がゲスト (`guest` または `annonymous`) かどうか (`1`: ゲスト, `0`: ゲストでない) |- |
| `count` | int | ⭕️ | 過去2秒間での、同じホストへの接続回数 |- |
| `srv_count` | int | ⭕️ | 過去2秒間での、同じサービスへの接続回数 |- |
| `serror_rate` | real | ⭕️ | `SYN`エラーの接続割合 |- |
| `srv_serror_rate` | real | ⭕️ | サービスに対する`SYN`エラーの接続割合 |- |
| `rerror_rate` | real | ⭕️ | `REJ`エラーの接続割合 |- |
| `srv_rerror_rate` | real | ⭕️ | サービスに対する`REJ`エラーの接続割合 |- |
| `same_srv_rate` | real | ⭕️ | 同じサービスへの接続割合 |- |
| `diff_srv_rate` | real | ⭕️ | 異なるサービスへの接続割合 |- |
| `srv_diff_host_rate` | real | ⭕️ | 異なるホストへの接続割合 |- |
| `dst_host_count` | int | ⭕️ | 同一宛先ホストへの接続回数 |- |
| `dst_host_srv_count` | int | ⭕️ | 同一宛先ホストの同一サービスへの接続回数 |- |
| `class` | string | ❌ | 通信のクラス (`"normal"`, `"attack"` のいずれか) | ✅ |


### test.csv

テスト用データです。

各カラムは `train.csv` と同じですが、`class` が含まれていません。

### train-tiny.csv

train.csv のうち欠損値が含まれない行を抽出した **train.csvのサブセットです。**

### test-fillna.csv 

test.csv について、欠損値を全て0で埋めたデータです。

### sample_submission.csv

提出用のサンプルファイルです。

`id` と `pred` の2つのカラムからなります。

`id` は `test.csv` の `id` と完全に一致しています。

`pred` には `normal` または `attack` がランダムに割り当てられています。

"""




def select_data(env):
    datasets = Constants.DATASETS
    st.write(HEAD, unsafe_allow_html=True)
    
    st.write("### Download")
    
    for name, url in datasets.items():
        st.write(
            f"""
            ### {name}
            [Download {name}]({url})
            """
        )

