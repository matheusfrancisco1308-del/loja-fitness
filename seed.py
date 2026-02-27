from app import app
from models import db, Produto

produtos = [
    # ================= FEMININO =================
    {
        "nome": "Conj. Vestido e Shorts Wide",
        "preco": 219.90,
        "img": "vestido-shorts-wide.jpg",
        "categoria": "Feminino",
        "tamanhos": "P,M,G",
        "marca": "LIVE!"
    },

{
    "nome": "Body Allure Adaptiv",
    "preco": 189.90,
    "img": "body-allure-adaptiv.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

{
    "nome": "Macacão Allure Adaptiv",
    "preco": 259.90,
    "img": "macacao-allure-adaptiv.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

{
    "nome": "Macaquinho Shorts Twist Softness",
    "preco": 239.90,
    "img": "macaquinho-shorts-twist-softness.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

{
    "nome": "Saia LIVE!",
    "preco": 169.90,
    "img": "saia-live.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

{
    "nome": "Jaqueta Balloon Air Vast",
    "preco": 299.90,
    "img": "jaqueta-balloon-air.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

{
    "nome": "Top Cut Out Fit",
    "preco": 119.90,
    "img": "top-cutout-fit.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

{
    "nome": "Legging Core Fit",
    "preco": 179.90,
    "img": "legging-core-fit.jpg",
    "categoria": "Feminino",
    "tamanhos": "P,M,G",
    "marca": "LIVE!"
},

# ================= MASCULINO =================
{
    "nome": "Camiseta ML Train Comfy",
    "preco": 129.90,
    "img": "camiseta-ml-train-comfy-men.jpeg",
    "categoria": "Masculino",
    "tamanhos": "P,M,G,GG",
    "marca": "LIVE!"
},

{
    "nome": "Camiseta Train Comfy",
    "preco": 119.90,
    "img": "camiseta-train-comfy-men.jpeg",
    "categoria": "Masculino",
    "tamanhos": "P,M,G,GG",
    "marca": "LIVE!"
},

{
    "nome": "Regata Train Comfy",
    "preco": 109.90,
    "img": "regata-train-comfy-men.jpeg",
    "categoria": "Masculino",
    "tamanhos": "P,M,G,GG",
    "marca": "LIVE!"
}
   
]

with app.app_context():
    db.create_all()  # <- cria as tabelas se não existirem

    Produto.query.delete()
    db.session.commit()

    for p in produtos:
        db.session.add(Produto(**p))
    db.session.commit()

print("Banco populado com sucesso!")
