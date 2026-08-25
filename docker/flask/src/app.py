import os
import time
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
                for item in items:
                    if item["stock"]<0:
                        item["stock"]=0
                # 取得したデータをデバッグレベルでログに出力
                logging.debug(items)
                # データベースからデータを取得してテンプレート（HTMLの土台）に渡す
                return render_template("index.html", items=items)
            except Exception as e:
                return jsonify({"db": "error", "detail": str(e)}), 500


@app.route("/buy", methods=["POST"])
def buy():
    data = request.get_json()
    # 同時アクセスを再現しやすいように5秒待機させる
    time.sleep(5)
    # POSTで送られてきたデータをデバッグログに出力
    logging.debug(data)
    id = int(data.get("id"))
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # 注文を登録
        cur.execute("INSERT INTO public.orders (item_id, quantity, status) VALUES (%s, 1, 'PAID') RETURNING id", (id,))
        order_id = cur.fetchone()['id']
        # 決済を登録
        cur.execute("INSERT INTO public.payments (order_id, amount, status) VALUES (%s, 1000, 'SUCCESS')", (order_id,))
        # リクエスト対象の在庫を減らす
        cur.execute("UPDATE public.items SET stock = stock - 1 WHERE id = %s AND stock >0 RETURNING stock", (id,))
        item = cur.fetchone()
        if item is None:
            conn.rollback()
            conn.close()
            return jsonify({"message":"在庫切れです"}),200
        # SQLを実行
        conn.commit()
        # 実行結果からデータを取得
        conn.close()
        # 取得したデータをデバッグレベルでログに出力
        logging.debug(item)
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"db": "error", "detail": str(e)}), 500
    message = "購入しました"
    logging.debug(message + "　残在庫数：" + str(item["stock"]))
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
    isDebug = LOG_LEVEL == "DEBUG"
    app.run(host="0.0.0.0", port=5000, debug=isDebug)
