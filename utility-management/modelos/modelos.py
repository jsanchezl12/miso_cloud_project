from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Utilidad(db.Model):
    __tablename__ = 'utilidad'

    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer)
    idOferta = db.Column(db.Integer)
    idTrayecto = db.Column(db.Integer)
    idPost = db.Column(db.Integer)
    utilidadOferta = db.Column(db.Integer)


class UtilidadSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Utilidad
        include_relationships = True
        load_instance = True