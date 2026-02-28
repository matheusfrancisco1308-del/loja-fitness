from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from models import db, Produto
import urllib.parse
import os

app = Flask(__name__)
app.secret_key = "sensuale_fitness_123"

# banco dentro do /instance (funciona local e no Render)
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "sensuale.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def seed_if_empty():
    # se já tem produtos, não faz nada
    if Produto.query.count() > 0:
        return

    produtos = [
        # FEMININO
        {"nome":"Conj. Vestido e Shorts Wide", "preco":219.90, "img":"vestido-shorts-wide.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Body Allure Adaptiv", "preco":189.90, "img":"body-allure-adaptiv.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Macacão Allure Adaptiv", "preco":259.90, "img":"macacao-allure-adaptiv.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Macaquinho Shorts Twist Softness", "preco":239.90, "img":"macaquinho-shorts-twist-softness.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Saia LIVE!", "preco":169.90, "img":"saia-live.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Jaqueta Balloon Air Vast", "preco":299.90, "img":"jaqueta-balloon-air.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Top Cut Out Fit", "preco":119.90, "img":"top-cutout-fit.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},
        {"nome":"Legging Core Fit", "preco":179.90, "img":"legging-core-fit.jpg",
         "categoria":"Feminino", "tamanhos":"P,M,G", "marca":"LIVE!"},

        # MASCULINO
        {"nome":"Camiseta ML Train Comfy", "preco":129.90, "img":"camiseta-ml-train-comfy-men.jpeg",
         "categoria":"Masculino", "tamanhos":"P,M,G,GG", "marca":"LIVE!"},
        {"nome":"Camiseta Train Comfy", "preco":119.90, "img":"camiseta-train-comfy-men.jpeg",
         "categoria":"Masculino", "tamanhos":"P,M,G,GG", "marca":"LIVE!"},
        {"nome":"Regata Train Comfy", "preco":109.90, "img":"regata-train-comfy-men.jpeg",
         "categoria":"Masculino", "tamanhos":"P,M,G,GG", "marca":"LIVE!"},
    ]

    for p in produtos:
        db.session.add(Produto(**p))
    db.session.commit()


# ✅ cria tabelas e popula se estiver vazio
with app.app_context():
    db.create_all()
    seed_if_empty()


def cart_count():
    cart = session.get("cart", [])
    return sum(int(item.get("qty", 1)) for item in cart)


@app.route("/")
def home():
    marca = request.args.get("marca")
    q = Produto.query.filter_by(categoria="Feminino")
    if marca:
        q = q.filter_by(marca=marca)
    produtos = q.all()

    return render_template(
        "index.html",
        produtos=produtos,
        cart_count=cart_count(),
        marca_selecionada=marca,
        categoria="Feminino",
    )


@app.route("/masculino")
def masculino():
    marca = request.args.get("marca")
    q = Produto.query.filter_by(categoria="Masculino")
    if marca:
        q = q.filter_by(marca=marca)
    produtos = q.all()

    return render_template(
        "index.html",
        produtos=produtos,
        cart_count=cart_count(),
        marca_selecionada=marca,
        categoria="Masculino",
    )


@app.route("/add_to_cart/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    tamanho = request.form.get("tamanho")
    if not tamanho:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"ok": False, "error": "Selecione um tamanho."}), 400
        return redirect(request.referrer or url_for("home"))

    cart = session.get("cart", [])

    for item in cart:
        if item["id"] == pid and item["tamanho"] == tamanho:
            item["qty"] += 1
            session["cart"] = cart
            session.modified = True
            break
    else:
        cart.append({"id": pid, "tamanho": tamanho, "qty": 1})
        session["cart"] = cart
        session.modified = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"ok": True, "cart_count": cart_count()})

    return redirect(request.referrer or url_for("home"))


@app.route("/checkout")
def checkout():
    cart = session.get("cart", [])
    if not cart:
        return render_template("checkout.html", itens=[], total=0, cart_count=0)

    ids = [item["id"] for item in cart]
    produtos = Produto.query.filter(Produto.id.in_(ids)).all()
    by_id = {p.id: p for p in produtos}

    itens = []
    total = 0.0

    for item in cart:
        p = by_id.get(item["id"])
        if not p:
            continue

        subtotal = float(p.preco) * int(item["qty"])
        total += subtotal

        itens.append({
            "id": p.id,
            "nome": p.nome,
            "img": p.img,
            "preco": float(p.preco),
            "tamanho": item["tamanho"],
            "qty": item["qty"],
            "subtotal": subtotal
        })

    return render_template("checkout.html", itens=itens, total=total, cart_count=cart_count())


@app.route("/finalizar")
def finalizar():
    cart = session.get("cart", [])
    if not cart:
        return redirect(url_for("home"))

    ids = [item["id"] for item in cart]
    produtos = Produto.query.filter(Produto.id.in_(ids)).all()
    by_id = {p.id: p for p in produtos}

    linhas = ["Olá, quero finalizar meu pedido:\n"]
    total = 0.0

    for item in cart:
        p = by_id.get(item["id"])
        if not p:
            continue

        subtotal = float(p.preco) * int(item["qty"])
        total += subtotal
        linhas.append(f"- {p.nome} | Tam: {item['tamanho']} | Qtd: {item['qty']} | R$ {subtotal:.2f}")

    linhas.append(f"\nTotal: R$ {total:.2f}")
    mensagem = "\n".join(linhas)

    numero = "5583999141449"
    url = f"https://wa.me/{numero}?text=" + urllib.parse.quote(mensagem)
    return redirect(url)


@app.route("/cart/inc/<int:pid>/<tamanho>", methods=["POST"])
def cart_inc(pid, tamanho):
    cart = session.get("cart", [])
    for item in cart:
        if item["id"] == pid and item["tamanho"] == tamanho:
            item["qty"] += 1
            break
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("checkout"))


@app.route("/cart/dec/<int:pid>/<tamanho>", methods=["POST"])
def cart_dec(pid, tamanho):
    cart = session.get("cart", [])
    for item in list(cart):
        if item["id"] == pid and item["tamanho"] == tamanho:
            item["qty"] -= 1
            if item["qty"] <= 0:
                cart.remove(item)
            break
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("checkout"))


@app.route("/cart/remove/<int:pid>/<tamanho>", methods=["POST"])
def cart_remove(pid, tamanho):
    cart = session.get("cart", [])
    cart = [i for i in cart if not (i["id"] == pid and i["tamanho"] == tamanho)]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("checkout"))


if __name__ == "__main__":
    app.run(debug=True)
