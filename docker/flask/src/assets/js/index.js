(() => {
  document.querySelectorAll('button[name="buy"]').forEach((el) => {

    el.onclick = async () => {

      try {

        const item = el.closest(".whole").querySelector(".item");

        const id = item.dataset.id;

        const res = await fetch("/buy", {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            id: id
          })
        });

        const data = await res.json();

        if (res.status !== 200) {
          alert("購入処理に失敗しました。");
          return;
        }

        alert(data.message);

        const whole = el.closest(".whole");

        const stock = whole.querySelector(".stock");

        if (data.stock === 0) {

          stock.innerHTML = `
            <p class="sold-out">
              SOLD OUT
            </p>
          `;

          el.innerText = "SOLD OUT";
          el.disabled = true;

        } else {

          stock.innerHTML = `
            <p class="${data.stock <= 3 ? "low-stock" : ""}">
              残り
              <span>${data.stock}</span>
              個
            </p>
          `;

        }

      } catch (error) {

        console.error(error);

        alert("通信エラーが発生しました。");

      }

    };

  });
})();