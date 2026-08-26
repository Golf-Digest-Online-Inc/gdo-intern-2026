(() => {

    document
        .querySelectorAll(".cancel-button")
        .forEach((button) => {

            button.onclick = async () => {

                const card =
                    button.closest(".order-card");

                const orderId =
                    card.dataset.orderId;


                // --------------------------------
                // 確認
                // --------------------------------

                const confirmed = confirm(
                    "この注文をキャンセルしますか？"
                );


                if (!confirmed) {
                    return;
                }


                // --------------------------------
                // ボタンを無効化
                // --------------------------------

                button.disabled = true;

                button.innerText =
                    "キャンセル処理中...";


                try {

                    const res = await fetch(
                        "/cancel",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                order_id: orderId
                            })
                        }
                    );


                    const data =
                        await res.json();


                    if (!res.ok) {

                        alert(
                            data.message ||
                            "キャンセルに失敗しました。"
                        );

                        button.disabled = false;

                        button.innerText =
                            "この注文をキャンセル";

                        return;
                    }


                    // --------------------------------
                    // 表示をキャンセル済みに変更
                    // --------------------------------

                    const status =
                        card.querySelector(".status");


                    status.classList.remove(
                        "completed"
                    );

                    status.classList.add(
                        "cancelled"
                    );

                    status.innerText =
                        "CANCELLED";


                    button.remove();


                    alert(
                        data.message
                    );


                } catch (error) {

                    console.error(error);

                    alert(
                        "通信エラーが発生しました。"
                    );


                    button.disabled = false;

                    button.innerText =
                        "この注文をキャンセル";
                }

            };

        });

})();