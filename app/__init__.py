from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    from app.models import Produto, Usuario

    from app.main import main_bp
    from app.produtos import produtos_bp
    from app.usuarios import usuarios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app