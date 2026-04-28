class SwaggerConfig:
    """Configurações do Swagger/OpenAPI"""

    # Configurações básicas da API
    API_TITLE = "API do Sistema de Ecommerce"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.0"

    # Configurações de rotas
    OPENAPI_URL_PREFIX = "/openapi"
    OPENAPI_SWAGGER_UI_PATH = "/apidocs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configurações adicionais (opcionais)
    OPENAPI_SWAGGER_UI_CONFIG = {
        "docExpansion": "list",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True
    }

    # Informações da API (opcional)
    OPENAPI_INFO = {
        "description": "API para gerenciamento de e-commerce",
        "contact": {
            "name": "Suporte",
            "email": "suporte@ecommerce.com",
            "url": "https://ecommerce.com/support"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }