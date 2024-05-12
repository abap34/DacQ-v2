## Usage


ビルド

```sh
docker-compose build
```

起動

```sh
docker-compose up
```

停止

```sh
docker-compose down
```

DBの初期化

```sh
docker volume rm dacq-v2_mariadb_data
```

## Setup

- `static/label.csv` に正解データを置く
  - `id`, `label` の2列 (`backend/const.py` で指定されてる
- `static/team_setting.csv` にチームの設定を置く
  - `id`, `user1`, `user2`, `user3`, の4列
- `static/rules.md` にルールを置く
