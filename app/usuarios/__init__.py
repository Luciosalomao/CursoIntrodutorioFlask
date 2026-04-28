from apiflask import APIBlueprint

usuarios_bp = APIBlueprint('usuarios', __name__)

from . import routes