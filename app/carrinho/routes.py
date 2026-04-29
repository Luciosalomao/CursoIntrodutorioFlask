from flask import jsonify
from sqlalchemy.testing.pickleable import User
from app import db

from app.models.produto import Produto
from flask_login import login_required, current_user
from . import carrinho_bp
from ..models import Usuario, ItemCarrinho


# =========================
# ADICIONAR ITEM CARRINHO
# =========================
@carrinho_bp.post('/adicionar/<int:produto_id>')
@carrinho_bp.doc(security=[{"SessionAuth": []}])
@login_required
def adicionar_item(produto_id):
    usuario = Usuario.query.get(int(current_user.id))
    produto = Produto.query.get(produto_id)

    if usuario and produto:
        item_carrinho = ItemCarrinho(usuario_id=usuario.id, produto_id=produto.id)
        db.session.add(item_carrinho)
        db.session.commit()

        return jsonify({'message': 'Item adicionado com sucesso'})

    else:
        return jsonify({'message': 'Falha ao adicionar item no carrinho'}), 400


# =========================
# REMOVER ITEM CARRINHO
# =========================
@carrinho_bp.delete('/remover/<int:produto_id>')
@carrinho_bp.doc(security=[{"SessionAuth": []}])
@login_required
def remover_item(produto_id):
    item_carrinho = ItemCarrinho.query.filter_by(usuario_id=current_user.id, produto_id=produto_id).first()
    if item_carrinho:
        db.session.delete(item_carrinho)
        db.session.commit()
        return jsonify({'message': 'Item removido com sucesso'})
    else:
        return jsonify({'messsage': 'Falha ao remover item no carrinho'}), 400

# =========================
# LISTAR ITENS CARRINHO
# =========================
@carrinho_bp.get('/')
@carrinho_bp.doc(security=[{"SessionAuth": []}])
@login_required
def view_carrinho():
    usuario = Usuario.query.get(current_user.id)
    itens_carrinho = usuario.carrinho
    carrinho_data = []
    for item in itens_carrinho:
        carrinho_data.append({
            'item_id': item.id,
            'produto_id': item.produto.id,
            'nome': item.produto.nome,
            'preco': item.produto.preco,
            'descricao': item.produto.descricao
        })

    return jsonify({
        'nome': usuario.nome,
        'mensagem': 'Itens no carrinho',
        'total_itens': len(carrinho_data),
        'itens': carrinho_data
    })