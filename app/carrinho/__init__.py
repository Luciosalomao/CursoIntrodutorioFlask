from apiflask import APIBlueprint

carrinho_bp = APIBlueprint('carrinho', __name__)

from . import routes