(() => {

  // 購入確認ポップアップ
  const modal = document.querySelector("#purchase-modal");

  const modalItemName = document.querySelector("#modal-item-name");

  const cancelButton = document.querySelector("#cancel-button");

  const confirmButton = document.querySelector("#confirm-button");


  // 現在購入しようとしている商品
  let selectedItem = null;


  // 購入ボタン
  document.querySelectorAll('button[name="buy"]').forEach((button) => {

    button.onclick = () => {

      // 商品カードを取得
      selectedItem = button.closest(".whole");

      // 商品名を取得
      const name =
        selectedItem.querySelector(".name p").innerText;

      // ポップアップに商品名を表示
      modalItemName.innerText = name;

      // ポップアップを表示
      modal.style.display = "flex";
    };

  });


  // キャンセルボタン
  cancelButton.onclick = () => {

    modal.style.display = "none";

    selectedItem = null;

  };


  // 購入するボタン
  confirmButton.onclick = async () => {

    // 商品が選択されていなければ何もしない
    if (!selectedItem) {
      return;
    }


    // 商品ID
    const id =
      selectedItem.querySelector(".item").dataset.id;


    // 購入処理
    const res = await fetch("/buy", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        id: id
      })

    });


    if (res.status === 200) {

      const data = await res.json();


      // 在庫を更新
      selectedItem.querySelector(".stock span").innerText =
        data.stock;


      // ポップアップを閉じる
      modal.style.display = "none";


      // 購入結果を表示
      alert(data.message);


      selectedItem = null;

    }

  };

})();