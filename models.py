from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)  # Feminino/Masculino
    tamanhos = db.Column(db.String(50), nullable=False)   # "P,M,G,GG"
    marca = db.Column(db.String(30), nullable=False)      # "LIVE!", "LUPO", "CAJU BRASIL"

    def __repr__(self):
        return f"<Produto {self.nome}>"
    