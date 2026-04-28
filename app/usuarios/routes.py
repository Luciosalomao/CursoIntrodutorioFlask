from app import db
from app.models.usuario import Usuario
from flask_login import login_user, logout_user, login_required, current_user
from . import usuarios_bp
from .schemas import (
    UsuarioSchema, UsuarioCreateSchema, UsuarioUpdateSchema,
    LoginSchema, UsuarioResponseSchema
)

# =========================
# LISTAR USUÁRIOS
# =========================
@usuarios_bp.get('/')
@usuarios_bp.doc(security=[{"SessionAuth": []}])
@login_required
@usuarios_bp.output(UsuarioSchema(many=True))
def listar_usuarios():
    return Usuario.query.all()


# =========================
# BUSCAR USUÁRIO
# =========================
@usuarios_bp.get('/<int:id>')
@usuarios_bp.doc(security=[{"SessionAuth": []}])
@login_required
@usuarios_bp.output(UsuarioSchema)
def buscar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return {
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado"
        }, 404

    return usuario


# =========================
# CRIAR USUÁRIO
# =========================
@usuarios_bp.post('/')
@usuarios_bp.input(UsuarioCreateSchema, arg_name="dados")
@usuarios_bp.output(UsuarioSchema, status_code=201)
def criar_usuario(dados):
    if Usuario.query.filter_by(email=dados['email']).first():
        return {
            "error": "duplicate_entry",
            "message": f"Email {dados['email']} ja esta cadastrado"
        }, 409

    usuario = Usuario(
        nome=dados['nome'],
        email=dados['email']
    )
    usuario.set_senha(dados['senha'])

    db.session.add(usuario)
    db.session.commit()

    return usuario


# =========================
# ATUALIZAR USUÁRIO
# =========================
@usuarios_bp.put('/<int:id>')
@usuarios_bp.doc(security=[{"SessionAuth": []}])
@usuarios_bp.input(UsuarioUpdateSchema, arg_name="dados")
@usuarios_bp.output(UsuarioSchema)
@login_required
def atualizar_usuario(id, dados):
    usuario = Usuario.query.get(id)

    if not usuario:
        return {
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado"
        }, 404

    if not dados:
        return {
            "error": "missing_fields",
            "message": "Pelo menos um campo deve ser enviado"
        }, 400

    if 'email' in dados and dados['email'] != usuario.email:
        if Usuario.query.filter_by(email=dados['email']).first():
            return {
                "error": "duplicate_entry",
                "message": f"Email {dados['email']} ja esta cadastrado"
            }, 409
        usuario.email = dados['email']

    if 'nome' in dados:
        usuario.nome = dados['nome']

    if 'senha' in dados:
        usuario.set_senha(dados['senha'])

    db.session.commit()
    return usuario


# =========================
# DELETAR USUÁRIO
# =========================
@usuarios_bp.delete('/<int:id>')
@usuarios_bp.doc(security=[{"SessionAuth": []}])
@login_required
def deletar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return {
            "error": "record_not_found",
            "message": f"Registro com ID {id} nao encontrado"
        }, 404

    db.session.delete(usuario)
    db.session.commit()

    return '', 204


# =========================
# LOGIN
# =========================
@usuarios_bp.post('/login')
@usuarios_bp.input(LoginSchema, arg_name="dados")
def login(dados):
    usuario = Usuario.query.filter_by(email=dados['email']).first()

    if not usuario or not usuario.check_senha(dados['senha']):
        return {
            "error": "invalid_credentials",
            "message": "Email ou senha invalidos"
        }, 401

    login_user(usuario, remember=dados.get('remember', False))

    return {
        "message": "Login realizado com sucesso",
        "usuario": UsuarioResponseSchema().dump(usuario)
    }


# =========================
# LOGOUT
# =========================
@usuarios_bp.post('/logout')
@usuarios_bp.doc(security=[{"SessionAuth": []}])
@login_required
def logout():
    logout_user()
    return {"message": "Logout realizado com sucesso"}


# =========================
# USUÁRIO ATUAL
# =========================
@usuarios_bp.get('/me')
@usuarios_bp.doc(security=[{"SessionAuth": []}])
@login_required
@usuarios_bp.output(UsuarioResponseSchema)
def usuario_atual():
    return current_user