(() => {
  document.querySelectorAll("button").forEach((el, i) => {
    const stock = el.closest(".whole").querySelector(".stock span").innerText;
    // if (stock > 0) {
      // 在庫が1以上の場合はボタンを有効にする
      // el.disabled = false;
      // ボタンにイベントを登録する（※イベント⇒クリックしたら、みたいな操作に対応した処理のこと）
      el.onclick = async (e) => {
        const res = await fetch("/buy", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ "id": el.closest(".whole").querySelector(".item").dataset.id })
        });

        if (res.status === 200) {
          const data = await res.json();
          el.closest(".whole").querySelector(".stock span").innerText = data.stock;
          alert(data.message);
        }
      };
    // }
  });
})();