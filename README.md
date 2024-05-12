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

## Setup

- `data/label.csv` に正解データを置く
  - `id`, `label` の2列 (`backend/const.py` で指定されてる
- `data/team_setting.csv` にチームの設定を置く
  - `id`, `user1`, `user2`, `user3`, の4列

