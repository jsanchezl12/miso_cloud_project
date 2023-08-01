from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from modelos.modelos import db
from vistas import VistaCrearOferta, VistaBuscarListarOferta, VistaConsultarOferta, VistaHealthCheck
import os

if 'DATABASE_URL' not in os.environ:
    DATABASE_URI = 'postgresql://postgres:DreamTeam123*@localhost:5432/postgres'
else:
    DATABASE_URI = os.environ['DATABASE_URL'] 
if DATABASE_URI is None or DATABASE_URI == '':
    DATABASE_URI = 'sqlite:///test_offer.db'
print('DATABASE_URI:',DATABASE_URI)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaCrearOferta, '/offers/')
api.add_resource(VistaBuscarListarOferta, '/offers')
api.add_resource(VistaConsultarOferta, '/offers/<string:id_oferta>')
api.add_resource(VistaHealthCheck, '/offers/ping')

jwt = JWTManager(app)

print(' * Ofertas corriendo ----------------')

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3003
    app.run(HOST, PORT, debug=True) 