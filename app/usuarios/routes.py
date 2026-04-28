from flask import jsonify, request
from app import db
from app.models.usuario import Usuario
from flask_login import login_user, logout_user, login_required, current_user
from . import usuarios_bp
from .schemas import (
    UsuarioSchema, UsuarioCreateSchema, UsuarioUpdateSchema,
    LoginSchema, UsuarioResponseSchema
)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
usuario_create_schema = UsuarioCreateSchema()
usuario_update_schema = UsuarioUpdateSchema()
login_schema = LoginSchema()
usuario_response_schema = UsuarioResponseSchema()


@usuarios_bp.route('/')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(usuarios_schema.dump(usuarios))


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

    return jsonify(usuario_schema.dump(usuario)), 200


@usuarios_bp.route('/', methods=['POST'])
def criar_usuario():
    dados = request.json

    erros = usuario_create_schema.validate(dados)
    if erros:
        return jsonify({
            "error": "invalid_data",
            "message": "Dados inválidos",
            "detalhes": erros
        }), 400

    dados_validados = usuario_create_schema.load(dados)

    usuario_existente = Usuario.query.filter_by(email=dados_validados['email']).first()
    if usuario_existente:
        return jsonify({
            "error": "duplicate_entry",
            "message": f"Email {dados_validados['email']} ja esta cadastrado"
        }), 409

    usuario = Usuario(
        nome=dados_validados['nome'],
        email=dados_validados['email']
    )
    usuario.set_senha(dados_validados['senha'])

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario_schema.dump(usuario)), 201


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

    erros = usuario_update_schema.validate(dados)
    if erros:
        return jsonify({
            "error": "invalid_data",
            "message": "Dados inválidos",
            "detalhes": erros
        }), 400

    dados_validados = usuario_update_schema.load(dados)

    if not dados_validados:
        return jsonify({
            "error": "missing_fields",
            "message": "Pelo menos um campo (nome, email ou senha) deve ser fornecido"
        }), 400

    if 'email' in dados_validados and dados_validados['email'] != usuario.email:
        usuario_existente = Usuario.query.filter_by(email=dados_validados['email']).first()
        if usuario_existente:
            return jsonify({
                "error": "duplicate_entry",
                "message": f"Email {dados_validados['email']} ja esta cadastrado"
            }), 409
        usuario.email = dados_validados['email']

    if 'nome' in dados_validados:
        usuario.nome = dados_validados['nome']

    if 'senha' in dados_validados:
        usuario.set_senha(dados_validados['senha'])

    db.session.commit()

    return jsonify(usuario_schema.dump(usuario)), 200


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

    erros = login_schema.validate(dados)
    if erros:
        return jsonify({
            "error": "invalid_data",
            "message": "Dados inválidos",
            "detalhes": erros
        }), 400

    dados_validados = login_schema.load(dados)

    usuario = Usuario.query.filter_by(email=dados_validados['email']).first()

    if not usuario or not usuario.check_senha(dados_validados['senha']):
        return jsonify({
            "error": "invalid_credentials",
            "message": "Email ou senha invalidos"
        }), 401

    login_user(usuario, remember=dados_validados.get('remember', False))

    return jsonify({
        "message": "Login realizado com sucesso",
        "usuario": usuario_response_schema.dump(usuario)
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
    return jsonify(usuario_response_schema.dump(current_user)), 200