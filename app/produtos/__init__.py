from flask import Blueprint

produtos_bp = Blueprint('produtos', __name__)

from . import routes