document.addEventListener("submit", async (e) => {
  const form = e.target;
  if (!form.classList.contains("add-to-cart-form")) return;

  e.preventDefault(); // não recarrega

  // valida tamanho (radio)
  const checked = form.querySelector('input[name="tamanho"]:checked');
  if (!checked) {
    alert("Selecione um tamanho antes de adicionar.");
    return;
  }

  try {
    const res = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { "X-Requested-With": "XMLHttpRequest" }
    });

    const data = await res.json();

    if (data.ok) {
      const badge = document.querySelector(".bag .badge");
      if (badge) badge.textContent = data.cart_count;
    } else {
      alert(data.error || "Não foi possível adicionar.");
    }
  } catch (err) {
    console.error(err);
    alert("Erro ao adicionar na sacola.");
  }
});