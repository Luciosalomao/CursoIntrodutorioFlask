from flask import request, g
from functools import wraps


def force_json_content_type(app):
    @app.before_request
    def set_content_type():
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.data and request.headers.get('Content-Type') != 'application/json':
                request.environ['CONTENT_TYPE'] = 'application/json'

    return app