from datetime import datetime, timedelta
import hashlib
import os
import requests
from flask import request
from flask_restful import Resource, reqparse
from dateutil.parser import parse
import json
import uuid

SECRET_TOKEN = ''
USER_MS = ''
SIDECARAPI_MS = ''
# Convertirlo en una variable de entorno
if 'SECRET_TOKEN' not in os.environ:
    SECRET_TOKEN = 'gcloudprojectg14'
    USER_MS = 'localhost:3000'
    SIDECARAPI_MS = 'localhost:3005'
else:
    SECRET_TOKEN = os.environ['SECRET_TOKEN']
    USER_MS = os.environ['USERS_PATH']
    SIDECARAPI_MS = os.environ['SIDECARAPI_PATH']

print(SECRET_TOKEN, flush=True)
print(USER_MS, flush=True)
print(SIDECARAPI_MS, flush=True)

if USER_MS == 'users':
    USER_MS = 'users:3000'
if SIDECARAPI_MS == 'sidecarapi':
    SIDECARAPI_MS = 'sidecarapi:3005'

print(' * USER_MS: {}'.format(USER_MS), flush=True)
print(' * SIDECARAPI_MS: {}'.format(SIDECARAPI_MS), flush=True)

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaWebhook(Resource):
    def post(self):
        data = request.get_json()
        print(data, flush=True)
        RUV = data['RUV']
        SCORE = data['score']
        token = f"{SECRET_TOKEN}:{RUV}:{SCORE}"
        sha_token = hashlib.sha256(token.encode()).hexdigest()
        print('-----------------------------------------------')
        print(token, flush=True)
        print(sha_token, flush=True)
        print('-----------------------------------------------')
        if sha_token != data['verifyToken']:
            print('Token no coincide', flush=True)
            return 'Token no corresponde al definido en el servicio', 401
        else:
            print('Token coincide', flush=True)
            email = ''
            status = ''
            if(data['status'] == "DELIVERED"):
                if (data["score"] >= 80):
                    status = "VERIFICADO"
                else:
                    status = "NO_VERIFICADO"
                user_confirmed_ms_url = 'http://{}/users'.format(USER_MS)
                body_user_confirmed = {
                    "id": data['userIdentifier'],
                    "status": status
                }
                user_confirmed = requests.put(user_confirmed_ms_url, json=body_user_confirmed)
                if user_confirmed.status_code != 201:
                    return user_confirmed.json(), user_confirmed.status_code
                data_user = user_confirmed.json()
                email = data_user['email']
                if email != '':
                    print(email , flush=True)
                    pubsubuser_url = 'http://{}/pubsubuser'.format(SIDECARAPI_MS)
                    bodyPubSub = {
                        "receiver": email,
                        "subject": "Verificación de identidad",
                        "body_mail": "Su verificación de identidad ha sido completada ["+ str(status) +"]. \nSu puntaje es: " + str(data["score"]) + ".\n"
                    }
                    pubsubuser = requests.post(pubsubuser_url, json=bodyPubSub)
                    if pubsubuser.status_code != 200:
                        return pubsubuser.json(), pubsubuser.status_code
                    return 'ok', 200
                else:
                    return 'No se puede confirmar el usuario', 401
        return 'ok', 200