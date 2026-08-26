let orderCount=0;
let totalPrice=0;

(() => {
  document.querySelectorAll("button[name='buy']").forEach((el, i) => {
    //const stock = el.closest(".whole").querySelector(".stock span").innerText;
    // if (stock > 0) {
      // 在庫が1以上の場合はボタンを有効にする
      // el.disabled = false;
      // ボタンにイベントを登録する（※イベント⇒クリックしたら、みたいな操作に対応した処理のこと）
      el.onclick = async (e) => {
        console.log("クリック");
        
        const res = await fetch("/buy", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ "id": el.closest(".whole").querySelector(".item").dataset.id })
        });

        if (res.status === 200) {
          const data = await res.json();
          el.closest(".whole").querySelector(".stock span").innerText = data.stock;

          const price = Number(
            el.closest(".whole").dataset.price
          );

          orderCount++;
          totalPrice += price;

          document.getElementById("order-count").innerText = orderCount;
          document.getElementById("total-price").innerText = totalPrice.toLocaleString();

          alert(data.message);
        }
      };
    // }
  });

})();

function filterItems(name) {
  console.debug("call filterItems");
  document.querySelectorAll(".whole").forEach(item=>{
    if(name==="all"){
      item.style.display="";
      return;
    }
    if(item.dataset.name.includes(name)){
      item.style.display="";
    }else{
      item.style.display="none";
    }
  });
};
