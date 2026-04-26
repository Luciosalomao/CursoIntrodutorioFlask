from flask import Blueprint, jsonify, request
from app import db
from app.models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(usuarios)


@usuarios_bp.route('/<int:id>')
def buscar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "usuario",
            "requested_id": id
        }), 422

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
def atualizar_usuario(id):
    dados = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "usuario",
            "requested_id": id
        }), 422

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
def deletar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado",
            "resource_type": "usuario",
            "requested_id": id
        }), 422

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

    return jsonify({
        "message": "Login realizado com sucesso",
        "usuario": usuario
    }), 200