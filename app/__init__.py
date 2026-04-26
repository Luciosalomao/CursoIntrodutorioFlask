from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    from app.models import Produto, Usuario

    from app.main.routes import main_bp
    from app.produtos.routes import produtos_bp
    from app.usuarios.routes import usuarios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app