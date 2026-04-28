from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    email = fields.Email(required=True)

class UsuarioCreateSchema(Schema):
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(required=True, load_only=True)

class UsuarioUpdateSchema(Schema):
    nome = fields.Str()
    email = fields.Email()
    senha = fields.Str(load_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    senha = fields.Str(required=True, load_only=True)
    remember = fields.Bool()

class UsuarioResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    email = fields.Email()