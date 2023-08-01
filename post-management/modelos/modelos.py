from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Publicacion(db.Model):
    __tablename__ = 'publicacion'

    id = db.Column(db.Integer, primary_key=True)
    routeId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    plannedStartDate = db.Column(db.DateTime)
    plannedEndDate = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)


class PublicacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Publicacion
        include_relationships = True
        load_instance = True