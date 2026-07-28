import os
import logging
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    static_folder="assets",
    static_url_path="/assets",
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    filename="/var/logs/app.log",
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(message)s"
)

DATABASE_URL = os.getenv("DATABASE_URL", "")

# 環境変数から取得したデータベース接続情報をログ出力
# DEBUGレベルでのログ出力にすることで、コードに記述が残っていても
# 出力設定がINFO以上の環境ではログ出力が行われないので、稼働環境にそのまま移しても問題がない
logging.debug("DATABASE_URL='" + DATABASE_URL + "'")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                # SQLを実行
                cur.execute("SELECT * FROM public.items ORDER BY id ASC")
                # 実行結果からデータを取得
                items = cur.fetchall()
                # 取得したデータをデバッグレベルでログに出力
                logging.debug(items)
                # データベースからデータを取得してテンプレート（HTMLの土台）に渡す
                return render_template("index.html", items=items)
            except Exception as e:
                return jsonify({"db": "error", "detail": str(e)}), 500


@app.route("/buy", methods=["POST"])
def buy():
    data = request.get_json()
    # POSTで送られてきたデータをデバッグログに出力
    logging.debug(data)
    id = int(data.get("id"))
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # 注文を登録
        cur.execute("INSERT INTO public.orders (item_id, quantity, status) VALUES (%s, 1, 'PAID') RETURNING id", (id,))
        conn.commit()
        order_id = cur.fetchone()['id']
        # 決済を登録
        cur.execute("INSERT INTO public.payments (order_id, amount, status) VALUES (%s, 1000, 'SUCCESS')", (order_id,))
        conn.commit()
        # リクエスト対象の在庫を減らす
        cur.execute("UPDATE public.items SET stock = stock - 1 WHERE id = %s", (id,))
        conn.commit()
        # SQLを実行
        cur.execute("SELECT * FROM public.items WHERE id = %s", (id,))
        # 実行結果からデータを取得
        item = cur.fetchone()
        # 取得したデータをデバッグレベルでログに出力
        logging.debug(item)
        conn.close()
    except Exception as e:
        return jsonify({"db": "error", "detail": str(e)}), 500
    message = "購入しました"
    logging.debug(message, item["stock"])
    return jsonify({"message": message, "stock": item["stock"]})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/db-check")
def db_check():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                cur.execute("SELECT * FROM public.items ORDER BY id ASC")
                rows = cur.fetchall()
                logging.debug(rows)
                return jsonify({"db": "connected", "rows": rows})
            except Exception as e:
                return jsonify({"db": "error", "detail": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
