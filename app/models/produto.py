from app import db
from dataclasses import dataclass

@dataclass
class Produto(db.Model):
    __tablename__ = 'produtos'

    id: int
    nome: str
    preco: float
    descricao: str

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'