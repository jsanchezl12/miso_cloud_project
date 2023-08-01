from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Oferta(db.Model):
    __tablename__ = 'oferta'

    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    description = db.Column(db.String(140))
    size = db.Column(db.String(500))
    fragile = db.Column(db.Boolean)
    offer = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)


class OfertaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Oferta
        include_relationships = True
        load_instance = True