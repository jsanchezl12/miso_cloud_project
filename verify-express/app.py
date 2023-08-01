from flask import Flask
from flask_restful import Api
from datetime import timedelta
import os
from vistas import VistaHealthCheck, VistaAgregarCola

app = Flask(__name__)
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaHealthCheck, '/ping')
api.add_resource(VistaAgregarCola, '/addTask')

print(' *** VERIFY-EXPRESS corriendo ----------------', flush=True)

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3007
    app.run(HOST, PORT, debug=True) 