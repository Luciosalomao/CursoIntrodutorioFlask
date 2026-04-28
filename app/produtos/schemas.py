from marshmallow import Schema, fields, validate

class ProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=True, validate=validate.Range(min=0))
    descricao = fields.Str(allow_none=True)
    estoque = fields.Int()

class ProdutoCreateSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=True, validate=validate.Range(min=0))
    descricao = fields.Str(allow_none=True)
    estoque = fields.Int()

class ProdutoUpdateSchema(Schema):
    nome = fields.Str(validate=validate.Length(min=1, max=100))
    preco = fields.Float(validate=validate.Range(min=0))
    descricao = fields.Str(allow_none=True)
    estoque = fields.Int()

