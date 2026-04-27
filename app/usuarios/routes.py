import os

from flask import Blueprint, jsonify, request, session
from app import db
from app.models.usuario import Usuario
from flask_login import login_user, logout_user, login_required, current_user

usuarios_bp = Blueprint('usuarios', __name__)

DOCS_PATH = os.path.join(os.path.dirname(__file__), 'docs')

@usuarios_bp.route('/')
@login_required
def listar_usuarios():

    usuarios = Usuario.query.all()
    return jsonify(usuarios)


@usuarios_bp.route('/<int:id>')
@login_required
def buscar_usuario(id):

    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "usuario",
            "requested_id": id
        }), 404

    return jsonify(usuario), 200


@usuarios_bp.route('/', methods=['POST'])
def criar_usuario():

    dados = request.json

    if not dados.get('nome') or not dados.get('email') or not dados.get('senha'):
        return jsonify({
            "error": "missing_fields",
            "message": "nome, email e senha sao obrigatorios"
        }), 400

    usuario_existente = Usuario.query.filter_by(email=dados['email']).first()
    if usuario_existente:
        return jsonify({
            "error": "duplicate_entry",
            "message": f"Email {dados['email']} ja esta cadastrado"
        }), 409

    usuario = Usuario(
        nome=dados['nome'],
        email=dados['email']
    )
    usuario.set_senha(dados['senha'])

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario), 201


@usuarios_bp.route('/<int:id>', methods=['PUT'])
@login_required
def atualizar_usuario(id):

    dados = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "usuario",
            "requested_id": id
        }), 404

    if not dados.get('nome') and not dados.get('email') and not dados.get('senha'):
        return jsonify({
            "error": "missing_fields",
            "message": "Pelo menos um campo (nome, email ou senha) deve ser fornecido"
        }), 400

    if dados.get('email') and dados['email'] != usuario.email:
        usuario_existente = Usuario.query.filter_by(email=dados['email']).first()
        if usuario_existente:
            return jsonify({
                "error": "duplicate_entry",
                "message": f"Email {dados['email']} ja esta cadastrado"
            }), 409
        usuario.email = dados['email']

    if dados.get('nome'):
        usuario.nome = dados['nome']

    if dados.get('senha'):
        usuario.set_senha(dados['senha'])

    db.session.commit()

    return jsonify(usuario), 200


@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def deletar_usuario(id):

    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "usuario",
            "requested_id": id
        }), 404

    db.session.delete(usuario)
    db.session.commit()

    return '', 204


@usuarios_bp.route('/login', methods=['POST'])
def login():

    dados = request.json

    if not dados.get('email') or not dados.get('senha'):
        return jsonify({
            "error": "missing_fields",
            "message": "email e senha sao obrigatorios"
        }), 400

    usuario = Usuario.query.filter_by(email=dados['email']).first()

    if not usuario or not usuario.check_senha(dados['senha']):
        return jsonify({
            "error": "invalid_credentials",
            "message": "Email ou senha invalidos"
        }), 401

    login_user(usuario, remember=dados.get('remember', False))

    return jsonify({
        "message": "Login realizado com sucesso",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }), 200


@usuarios_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({
        "message": "Logout realizado com sucesso"
    }), 200


@usuarios_bp.route('/me', methods=['GET'])
@login_required
def usuario_atual():

    return jsonify({
        "id": current_user.id,
        "nome": current_user.nome,
        "email": current_user.email
    }), 200