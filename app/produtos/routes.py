from flask import Blueprint, jsonify, request
from app import db
from app.models.produto import Produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/')
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'preco': p.preco,
        'descricao': p.descricao
    } for p in produtos])

@produtos_bp.route('/<int:id>')
def buscar_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify({
        'id': produto.id,
        'nome': produto.nome,
        'preco': produto.preco,
        'descricao': produto.descricao
    })

@produtos_bp.route('/', methods=['POST'])
def criar_produto():
    dados = request.json
    produto = Produto(
        nome=dados['nome'],
        preco=dados['preco'],
        descricao=dados.get('descricao', '')
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto criado!', 'id': produto.id}), 201