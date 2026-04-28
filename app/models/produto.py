from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    estoque = db.Column(db.Integer, default=0, nullable=False)
    carrinho = db.relationship('ItemCarrinho', backref='produto', lazy=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'