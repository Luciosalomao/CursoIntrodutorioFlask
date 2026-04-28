from apiflask import APIBlueprint

produtos_bp = APIBlueprint('produtos', __name__)

from . import routes