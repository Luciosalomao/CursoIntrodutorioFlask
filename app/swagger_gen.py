import json

ENDPOINTS = {
    "/produtos": {
        "get": {
            "summary": "Lista todos os produtos",
            "responses": {"200": {"description": "Lista de produtos"}}
        },
        "post": {
            "summary": "Cria um novo produto",
            "responses": {"201": {"description": "Produto criado"}}
        }
    },
    "/produtos/{id}": {
        "get": {
            "summary": "Busca um produto pelo ID",
            "responses": {"200": {"description": "Produto encontrado"}}
        },
        "put": {
            "summary": "Atualiza um produto",
            "responses": {"200": {"description": "Produto atualizado"}}
        },
        "delete": {
            "summary": "Deleta um produto",
            "responses": {"204": {"description": "Produto deletado"}}
        }
    },
    "/usuarios": {
        "get": {
            "summary": "Lista todos os usuarios",
            "responses": {"200": {"description": "Lista de usuarios"}}
        },
        "post": {
            "summary": "Cria um novo usuario",
            "responses": {"201": {"description": "Usuario criado"}}
        }
    },
    "/usuarios/{id}": {
        "get": {
            "summary": "Busca um usuario pelo ID",
            "responses": {"200": {"description": "Usuario encontrado"}}
        },
        "put": {
            "summary": "Atualiza um usuario",
            "responses": {"200": {"description": "Usuario atualizado"}}
        },
        "delete": {
            "summary": "Deleta um usuario",
            "responses": {"204": {"description": "Usuario deletado"}}
        }
    },
    "/usuarios/login": {
        "post": {
            "summary": "Faz login do usuario",
            "responses": {"200": {"description": "Login realizado"}}
        }
    },
    "/usuarios/logout": {
        "post": {
            "summary": "Faz logout do usuario",
            "responses": {"200": {"description": "Logout realizado"}}
        }
    },
    "/usuarios/me": {
        "get": {
            "summary": "Retorna o usuario logado",
            "responses": {"200": {"description": "Usuario logado"}}
        }
    }
}


def generate_swagger_json():
    swagger = {
        "openapi": "3.0.0",
        "info": {
            "title": "API de Produtos e Usuarios",
            "version": "1.0.0"
        },
        "servers": [
            {"url": "http://localhost:5000", "description": "Servidor local"}
        ],
        "paths": ENDPOINTS
    }

    with open("app/static/swagger.json", "w", encoding="utf-8") as f:
        json.dump(swagger, f, indent=2, ensure_ascii=False)

    print("swagger.json gerado com sucesso!")


if __name__ == "__main__":
    generate_swagger_json()