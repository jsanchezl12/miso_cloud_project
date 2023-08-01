from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource, reqparse
from dateutil.parser import parse
from google.cloud import storage
from google.oauth2 import service_account
import uuid
import json

project_id = "gcloudprojectg14e2"
with open('gcloudprojectg14e2-3989e9906e60.json') as source:
    info = json.load(source)

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaArchiveEmail(Resource):
    def post(self):
        try:
            data = request.get_json()
            print('data', data)
            storage_credentials = service_account.Credentials.from_service_account_info(info)
            storage_client = storage.Client(project=project_id, credentials=storage_credentials)
            bucket_name = 'bucket_g14_miso'
            fileup_name = str(uuid.uuid1()) + '.txt'
            path_fileup = './vistas/files/' + fileup_name
            f = open(path_fileup,"w+")
            f.write(str(data))
            f.close()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(fileup_name)
            blob.upload_from_filename(path_fileup)
            link_file = 'https://storage.googleapis.com/' + bucket_name + '/' + fileup_name
            return {'file_link': link_file}, 200
        except Exception as err:
            print("Error archiving email: %s" % err)
            return 'Error archivando el correo', 500