from flask import Flask
from flask_restful import Api
from datetime import timedelta
import os
from vistas import VistaHealthCheck, VistaArchiveEmail

app = Flask(__name__)
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaHealthCheck, '/ping')
api.add_resource(VistaArchiveEmail, '/archive_email')



print(' *** ARCHIVE-EMAIL corriendo ----------------', flush=True)

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3009
    app.run(HOST, PORT, debug=True) 