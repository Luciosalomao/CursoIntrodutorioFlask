from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from apiflask import APIFlask

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
cors = CORS()


def create_app():
    app = APIFlask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({
            "error": "unauthorized",
            "message": "Voce precisa estar logado para acessar este recurso"
        }), 401

    login_manager.login_view = 'usuarios.login'
    login_manager.login_message = None
    login_manager.login_message_category = 'info'

    from app.models import Produto, Usuario
    from app.main import main_bp
    from app.produtos import produtos_bp
    from app.usuarios import usuarios_bp
    from app.carrinho import carrinho_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(carrinho_bp, url_prefix='/carrinho')

    return app