from app import db
from app.models.produto import Produto
from flask_login import login_required
from .schemas import ProdutoSchema, ProdutoCreateSchema, ProdutoUpdateSchema
from . import produtos_bp

# =========================
# LISTAR PRODUTOS
# =========================
@produtos_bp.get('/')
@produtos_bp.output(ProdutoSchema(many=True))
def listar_produtos():
    return Produto.query.all()


# =========================
# BUSCAR PRODUTO
# =========================
@produtos_bp.get('/<int:id>')
@produtos_bp.output(ProdutoSchema)
def buscar_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return {
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado"
        }, 404

    return produto


# =========================
# CRIAR PRODUTO
# =========================
@produtos_bp.post('/')
@produtos_bp.doc(security=[{"SessionAuth": []}])
@produtos_bp.input(ProdutoCreateSchema, arg_name="dados")
@produtos_bp.output(ProdutoSchema, status_code=201)
@login_required
def criar_produto(dados):
    produto = Produto(
        nome=dados['nome'],
        preco=dados['preco'],
        descricao=dados.get('descricao', ''),
        estoque=dados.get('estoque', 0)
    )

    db.session.add(produto)
    db.session.commit()

    return produto


# =========================
# ATUALIZAR PRODUTO
# =========================
@produtos_bp.put('/<int:id>')
@produtos_bp.doc(security=[{"SessionAuth": []}])
@produtos_bp.input(ProdutoUpdateSchema, arg_name="dados")
@produtos_bp.output(ProdutoSchema)
@login_required
def atualizar_produto(id, dados):
    produto = Produto.query.get(id)

    if not produto:
        return {
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado"
        }, 404

    if 'nome' in dados:
        produto.nome = dados['nome']
    if 'preco' in dados:
        produto.preco = dados['preco']
    if 'descricao' in dados:
        produto.descricao = dados['descricao']
    if 'estoque' in dados:
        produto.estoque = dados['estoque']

    db.session.commit()

    return produto


# =========================
# DELETAR PRODUTO
# =========================
@produtos_bp.delete('/<int:id>')
@produtos_bp.doc(security=[{"SessionAuth": []}])
@login_required
def deletar_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return {
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado"
        }, 404

    db.session.delete(produto)
    db.session.commit()

    return '', 204