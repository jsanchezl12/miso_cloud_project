from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from vistas import VistaHealthCheck, VistaPublicPost, VistaPublicOffer, VistaSearchPost, VistaCrearUsuario, VistaGeneracionToken, VistaInfoUsuario, VistaPubSubUser, VistaManual, VistaInfoBaseUser


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()

cors = CORS(app)
api = Api(app)
api.add_resource(VistaHealthCheck, '/ping')
api.add_resource(VistaPublicPost, '/public/posts')
api.add_resource(VistaPublicOffer, '/public/posts/<int:id>/offers')
api.add_resource(VistaSearchPost, '/public/posts/<int:id>')
api.add_resource(VistaCrearUsuario, '/users/')
api.add_resource(VistaManual, '/users/manual-verification')
api.add_resource(VistaGeneracionToken, '/users/auth')
api.add_resource(VistaInfoUsuario, '/users/me')
api.add_resource(VistaPubSubUser, '/pubsubuser')
api.add_resource(VistaInfoBaseUser, '/users/user_base')

jwt = JWTManager(app)

print(' * UTILITY MANAGEMENT corriendo ----------------')

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3005
    app.run(HOST, PORT, debug=True) 