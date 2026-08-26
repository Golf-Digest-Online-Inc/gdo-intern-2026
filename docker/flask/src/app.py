import os
import time
import logging
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


logging.debug("DATABASE_URL='" + DATABASE_URL + "'")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


# ========================================
# 商品一覧
# ========================================

@app.route("/")
def index():

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            try:

                cur.execute(
                    """
                    SELECT *
                    FROM public.items
                    ORDER BY id ASC
                    """
                )

                items = cur.fetchall()

                # 在庫がマイナスの場合は画面上では0として表示
                for item in items:
                    if item["stock"] < 0:
                        item["stock"] = 0

                logging.debug(items)

                return render_template(
                    "index.html",
                    items=items
                )

            except Exception as e:

                return jsonify({
                    "db": "error",
                    "detail": str(e)
                }), 500


# ========================================
# 注文履歴
# ========================================

@app.route("/orders")
def orders():

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            try:

                cur.execute(
                    """
                    SELECT
                        orders.id AS order_id,
                        orders.quantity,
                        orders.status AS order_status,
                        orders.item_id,
                        items.name AS item_name,
                        items.image,
                        payments.amount,
                        payments.status AS payment_status
                    FROM public.orders

                    JOIN public.items
                        ON orders.item_id = items.id

                    JOIN public.payments
                        ON orders.id = payments.order_id

                    ORDER BY orders.id DESC
                    """
                )

                orders = cur.fetchall()

                return render_template(
                    "orders.html",
                    orders=orders
                )

            except Exception as e:

                return jsonify({
                    "db": "error",
                    "detail": str(e)
                }), 500


# ========================================
# 購入
# ========================================

@app.route("/buy", methods=["POST"])
def buy():

    data = request.get_json()

    if not data or data.get("id") is None:
        return jsonify({
            "message": "商品IDが指定されていません"
        }), 400

    try:
        item_id = int(data.get("id"))
    except (TypeError, ValueError):
        return jsonify({
            "message": "商品IDが不正です"
        }), 400


    # 同時アクセスを再現するための待機
    time.sleep(5)


    logging.debug(data)


    conn = None

    try:

        conn = get_connection()

        cur = conn.cursor(
            cursor_factory=RealDictCursor
        )


        # ----------------------------------------
        # 在庫を1つ減らす
        # ----------------------------------------

        cur.execute(
            """
            UPDATE public.items

            SET stock = stock - 1

            WHERE id = %s
            AND stock > 0

            RETURNING stock, price
            """,
            (item_id,)
        )


        item = cur.fetchone()


        # 在庫切れ
        if item is None:

            conn.rollback()

            return jsonify({
                "message": "在庫切れです",
                "stock": 0
            }), 200


        # ----------------------------------------
        # 注文登録
        # ----------------------------------------

        cur.execute(
            """
            INSERT INTO public.orders
            (
                item_id,
                quantity,
                status
            )

            VALUES
            (
                %s,
                1,
                'PAID'
            )

            RETURNING id
            """,
            (item_id,)
        )


        order_id = cur.fetchone()["id"]


        # ----------------------------------------
        # 決済登録
        # ----------------------------------------

        cur.execute(
            """
            INSERT INTO public.payments
            (
                order_id,
                amount,
                status
            )

            VALUES
            (
                %s,
                %s,
                'SUCCESS'
            )
            """,
            (
                order_id,
                item["price"]
            )
        )


        # ----------------------------------------
        # 確定
        # ----------------------------------------

        conn.commit()


        logging.debug(item)


        return jsonify({
            "message": "購入しました",
            "stock": item["stock"]
        })


    except Exception as e:

        if conn is not None:
            conn.rollback()

        logging.exception("購入処理でエラーが発生しました")


        return jsonify({
            "db": "error",
            "message": "購入処理に失敗しました",
            "detail": str(e)
        }), 500


    finally:

        if conn is not None:
            conn.close()


# ========================================
# キャンセル
# ========================================

@app.route("/cancel", methods=["POST"])
def cancel():

    data = request.get_json()


    if not data or data.get("order_id") is None:

        return jsonify({
            "message": "注文IDが指定されていません"
        }), 400


    try:

        order_id = int(
            data.get("order_id")
        )

    except (TypeError, ValueError):

        return jsonify({
            "message": "注文IDが不正です"
        }), 400


    conn = None


    try:

        conn = get_connection()

        cur = conn.cursor(
            cursor_factory=RealDictCursor
        )


        # ----------------------------------------
        # キャンセル対象の注文を取得
        # ----------------------------------------

        cur.execute(
            """
            SELECT
                orders.id,
                orders.item_id,
                orders.quantity,
                orders.status
            FROM public.orders

            WHERE orders.id = %s

            FOR UPDATE
            """,
            (order_id,)
        )


        order = cur.fetchone()


        # 注文が存在しない
        if order is None:

            conn.rollback()

            return jsonify({
                "message": "注文が見つかりません"
            }), 404


        # ----------------------------------------
        # すでにキャンセル済み
        # ----------------------------------------

        if order["status"] == "CANCELLED":

            conn.rollback()

            return jsonify({
                "message": "この注文はすでにキャンセルされています"
            }), 400


        # ----------------------------------------
        # 注文ステータス変更
        # ----------------------------------------

        cur.execute(
            """
            UPDATE public.orders

            SET status = 'CANCELLED'

            WHERE id = %s
            """,
            (order_id,)
        )


        # ----------------------------------------
        # 決済ステータス変更
        # ----------------------------------------

        cur.execute(
            """
            UPDATE public.payments

            SET status = 'CANCELLED'

            WHERE order_id = %s
            """,
            (order_id,)
        )


        # ----------------------------------------
        # 在庫を元に戻す
        # ----------------------------------------

        cur.execute(
            """
            UPDATE public.items

            SET stock = stock + %s

            WHERE id = %s

            RETURNING stock
            """,
            (
                order["quantity"],
                order["item_id"]
            )
        )


        item = cur.fetchone()


        # 商品が存在しない場合
        if item is None:

            conn.rollback()

            return jsonify({
                "message": "商品の在庫を戻せませんでした"
            }), 500


        # ----------------------------------------
        # 確定
        # ----------------------------------------

        conn.commit()


        logging.info(
            "注文キャンセル order_id=%s item_id=%s",
            order_id,
            order["item_id"]
        )


        return jsonify({
            "message": "注文をキャンセルしました",
            "stock": item["stock"]
        })


    except Exception as e:

        if conn is not None:
            conn.rollback()

        logging.exception(
            "キャンセル処理でエラーが発生しました"
        )


        return jsonify({
            "db": "error",
            "message": "キャンセル処理に失敗しました",
            "detail": str(e)
        }), 500


    finally:

        if conn is not None:
            conn.close()


# ========================================
# Health Check
# ========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok"
    })


# ========================================
# DB Check
# ========================================

@app.route("/db-check")
def db_check():

    with get_connection() as conn:

        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            try:

                cur.execute(
                    """
                    SELECT *
                    FROM public.items
                    ORDER BY id ASC
                    """
                )

                rows = cur.fetchall()

                logging.debug(rows)

                return jsonify({
                    "db": "connected",
                    "rows": rows
                })


            except Exception as e:

                return jsonify({
                    "db": "error",
                    "detail": str(e)
                }), 500


# ========================================
# 起動
# ========================================

if __name__ == "__main__":

    isDebug = LOG_LEVEL == "DEBUG"

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=isDebug
    )