from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Trayecto(db.Model):
    __tablename__ = 'trayecto'

    id = db.Column(db.Integer, primary_key=True)
    sourceAirportCode = db.Column(db.String(50))
    sourceCountry = db.Column(db.String(50))
    destinyAirportCode = db.Column(db.String(500))
    destinyCountry = db.Column(db.String(50))
    bagCost = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)


class TrayectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trayecto
        include_relationships = True
        load_instance = True