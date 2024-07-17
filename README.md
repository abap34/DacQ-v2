## Usage

### セットアップ

1. `app/const.py` の定数を設定する。
2. 必要なファイルを `app/static` 以下に配置する。
   - ラベルデータ
   - チーム設定データ
   - Public / Private の分割
3. `.env` に環境変数を設定する。
```sh
TOKEN_URL=
CLIENT_ID=
CLIENT_SECRET=
REDIRECT_URI=
AUTHORIZE_URL=
```



### ビルド

```sh
docker-compose build
```

### 起動

```sh
docker-compose up
```

### 終了

```sh
docker-compose down
```

### DB の初期化

```sh
docker volume rm dacq-v2_mariadb_data
```

### ポート

- `http://localhost:5001` (app)
- `http://localhost:8080` (adminer)