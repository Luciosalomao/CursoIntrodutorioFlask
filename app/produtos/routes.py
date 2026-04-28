from flask import jsonify, request
from app import db
from app.models.produto import Produto
from flask_login import login_required
from .schemas import ProdutoSchema, ProdutoCreateSchema, ProdutoUpdateSchema
from . import produtos_bp

produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)
produto_create_schema = ProdutoCreateSchema()
produto_update_schema = ProdutoUpdateSchema()


@produtos_bp.route('/')
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify(produtos_schema.dump(produtos))


@produtos_bp.route('/<int:id>')
def buscar_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "produto",
            "requested_id": id
        }), 404

    return jsonify(produto_schema.dump(produto)), 200


@produtos_bp.route('/', methods=['POST'])
@login_required
def criar_produto():
    dados = request.json

    erros = produto_create_schema.validate(dados)
    if erros:
        return jsonify({
            "error": "unprocessable_entity",
            "message": "Campos inválidos",
            "detalhes": erros
        }), 422

    dados_validados = produto_create_schema.load(dados)

    produto = Produto(
        nome=dados_validados['nome'],
        preco=dados_validados['preco'],
        descricao=dados_validados.get('descricao', ''),
        estoque = dados_validados.get('estoque', 0)
    )
    db.session.add(produto)
    db.session.commit()

    return jsonify(produto_schema.dump(produto)), 201


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
        }), 404

    erros = produto_update_schema.validate(dados)
    if erros:
        return jsonify({
            "error": "invalid_data",
            "message": "Dados inválidos",
            "detalhes": erros
        }), 400

    dados_validados = produto_update_schema.load(dados)

    if 'nome' in dados_validados:
        produto.nome = dados_validados['nome']
    if 'preco' in dados_validados:
        produto.preco = dados_validados['preco']
    if 'descricao' in dados_validados:
        produto.descricao = dados_validados['descricao']
    if 'estoque' in dados_validados:
        produto.estoque = dados_validados['estoque']

    db.session.commit()

    return jsonify(produto_schema.dump(produto)), 200


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
        }), 404

    db.session.delete(produto)
    db.session.commit()

    return '', 204