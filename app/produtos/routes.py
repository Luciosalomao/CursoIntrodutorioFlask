from flask import Blueprint, jsonify, request
from app import db
from app.models.produto import Produto
from flask_login import login_required, current_user

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/')
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify(produtos)


@produtos_bp.route('/<int:id>')
def buscar_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "produto",
            "requested_id": id
        }), 422

    return jsonify(produto), 200


@produtos_bp.route('/', methods=['POST'])
@login_required
def criar_produto():
    dados = request.json
    produto = Produto(
        nome=dados['nome'],
        preco=dados['preco'],
        descricao=dados.get('descricao', '')
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto), 201


@produtos_bp.route('/<int:id>', methods=['PUT'])
@login_required
def atualizar_produto(id):
    dados = request.json

    produto = Produto.query.get(id)

    if not produto:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "produto",
            "requested_id": id
        }), 422

    if not dados.get('nome') or not dados.get('preco'):
        return jsonify({
            "error": "missing_fields",
            "message": "nome e preco sao obrigatorios"
        }), 400

    produto.nome = dados['nome']
    produto.preco = dados['preco']
    produto.descricao = dados.get('descricao', '')
    db.session.commit()

    return jsonify(produto), 200


@produtos_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def deletar_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "produto",
            "requested_id": id
        }), 422

    db.session.delete(produto)
    db.session.commit()

    return '', 204