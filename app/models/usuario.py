from app import db
from dataclasses import dataclass, field
from flask_bcrypt import generate_password_hash, check_password_hash


@dataclass
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id: int
    nome: str
    email: str
    senha: str = field(repr=False, compare=False)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def set_senha(self, senha_plana):
        self.senha = generate_password_hash(senha_plana).decode('utf-8')

    def check_senha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)