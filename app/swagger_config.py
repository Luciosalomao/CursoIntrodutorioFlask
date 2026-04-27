SWAGGER_CONFIG = {
    'title': 'API do Sistema de Ecommerce',
    'description': 'API para gerenciamento de produtos com autenticação',
    'version': '1.0.0',
    'uiversion': 3,
    'specs_route': '/apidocs/',
    'openapi': '3.0.2',
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Token (formato: Bearer {token})'
        }
    },
    # Configurações adicionais opcionais
    'tags': [
        {
            'name': 'Produtos',
            'description': 'Operações relacionadas a produtos'
        },
        {
            'name': 'Usuários',
            'description': 'Operações relacionadas a usuários'
        },
        {
            'name': 'Autenticação',
            'description': 'Login e autenticação'
        }
    ],
    'definitions': {
        'Produto': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'nome': {'type': 'string'},
                'preco': {'type': 'number'},
                'descricao': {'type': 'string'},
                'categoria': {'type': 'string'},
                'estoque': {'type': 'integer'}
            }
        },
        'Usuario': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'email': {'type': 'string'},
                'nome': {'type': 'string'}
            }
        }
    }
}