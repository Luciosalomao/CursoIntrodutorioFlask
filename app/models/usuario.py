from app import db, login_manager
from dataclasses import dataclass, field
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@dataclass
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id: int
    nome: str
    email: str
    senha: str = field(repr=False, compare=False)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    carrinho = db.relationship('ItemCarrinho', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def set_senha(self, senha_plana):
        self.senha = generate_password_hash(senha_plana).decode('utf-8')

    def check_senha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)