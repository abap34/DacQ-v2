<!-- 記述例 -->

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
- sample_submission.csv : 提出用のサンプルファイル

### train.csv

学習用データです。

各レコードには、 xx に関する特徴量が含まれています。

以下のカラムからなります。

`class` が今回の目的変数です。

| カラム名 | データ型 | 欠損値 / ノイズ | 説明 | 目的変数 |
| --- | --- | --- | --- | --- |
| `id` | int | ❌ | データのID | - |
| `duration` | real | ⭕️ |  接続時間 (秒) | - ||
| `class` | string | ❌ | クラス (`"A"`, `"B"` のいずれか) | ✅ |


### test.csv

テスト用データです。

各カラムは `train.csv` と同じですが、`class` が含まれていません。

### sample_submission.csv

提出用のサンプルファイルです。

`id` と `pred` の2つのカラムからなります。

`id` は `test.csv` の `id` と完全に一致しています。

`pred` には `A` または `B` がランダムに割り当てられています。