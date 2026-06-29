# Docker 環境構成

Nginx + Flask + PostgreSQL の3コンテナ構成を docker compose で管理するリポジトリです。

## 構成

```
.
├── docker-compose.yml
├── nginx/
│   ├── Dockerfile        # Nginx 1.30.3
│   └── nginx.conf        # Flask へのリバースプロキシ設定
├── flask/
│   ├── Dockerfile        # Python 3.13-slim
│   ├── requirements.txt
│   └── src/
│       └── app.py        # Flask アプリ本体
```

## 前提条件

- Docker
- Docker Compose v2 以上

## 起動方法

```bash
docker compose up --build
```

停止・ボリューム削除:

```bash
docker compose down -v
```

## アクセス先

| エンドポイント | 説明 |
|---|---|
| `GET http://localhost:8080/` | 起動確認 |
| `GET http://localhost:8080/health` | ヘルスチェック |
| `GET http://localhost:8080/db-check` | PostgreSQL 接続確認 |

## 環境変数

| 変数名 | デフォルト値 | 説明 |
|---|---|---|
| `POSTGRES_USER` | `appuser` | DB ユーザー名 |
| `POSTGRES_PASSWORD` | `apppassword` | DB パスワード |
| `POSTGRES_DB` | `appdb` | DB 名 |

## 開発時のワークフロー

`flask/src/` 配下のファイルをコンテナにボリュームマウントしています。
`app.py` を保存すると Flask の自動リロードが働き、再ビルド不要で変更が反映されます。

`requirements.txt` を変更した場合のみ再ビルドが必要です。

```bash
docker compose up --build
```
