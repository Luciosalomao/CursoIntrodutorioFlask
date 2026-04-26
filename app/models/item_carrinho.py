from app import db
from dataclasses import dataclass

@dataclass
class ItemCarrinho(db.Model):
    __tablename__ = 'itens_carrinho'

    id: int
    usuario_id: int
    produto_id: int

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)

    def __repr__(self):
        return f'<ItemCarrinho Usuario:{self.usuario_id} Produto:{self.produto_id}>'