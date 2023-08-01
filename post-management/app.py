from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from modelos.modelos import db
from vistas import VistaCrearPublicacion, VistaBuscarPublicacion, VistaConsultarPublicacion, VistaHealthCheck
import os

if 'DATABASE_URL' not in os.environ:
    DATABASE_URI = 'postgresql://postgres:DreamTeam123*@localhost:50006/postgres'
    #DATABASE_URI = 'sqlite:///test_post.db'
else:
    DATABASE_URI = os.environ['DATABASE_URL'] 
if DATABASE_URI is None or DATABASE_URI == '':
    DATABASE_URI = 'sqlite:///test_post.db'

print('DATABASE_URI:',DATABASE_URI)
app = Flask(__name__)
#DATABASE_URI = 'postgresql://postgres:DreamTeam123*@host.docker.internal:50005/postgres'
#DATABASE_URI = 'postgresql://postgres:root@localhost:5432/postgres'
#DATABASE_URI = 'postgresql://postgres:DreamTeam123*@bd_userm:5432/postgres'
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
api.add_resource(VistaCrearPublicacion, '/posts/')
api.add_resource(VistaBuscarPublicacion, '/posts')
api.add_resource(VistaConsultarPublicacion, '/posts/<string:id_publicacion>')
api.add_resource(VistaHealthCheck, '/posts/ping')

jwt = JWTManager(app)

print(' * Post corriendo ----------------')

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3001
    app.run(HOST, PORT, debug=True) 