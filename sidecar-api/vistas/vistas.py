from datetime import datetime, timedelta
import hashlib
import os
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from dateutil.parser import parse
import json
import uuid
import time
import threading
from .pubsub import Publicador, ConcretePublicador, Subscriptor, ConcreteArchiveEmail, ConcreteEnviarCorreo

UTILITY_MS = ''
USER_MS = ''
EMAIL_MS = ''
BUCKET_MS = ''
TRUENATIVE_MS = ''
VERIFY_WEBHOOK_MS = ''
VERIFY_EXPRESS_MS = ''
SECRET_TOKEN = ''

if 'UTILITY_PATH' not in os.environ:
    SECRET_TOKEN = 'gcloudprojectg14'
    UTILITY_MS = 'localhost:3004'
    USER_MS = 'localhost:3000'
    EMAIL_MS = 'localhost:3008'
    BUCKET_MS = 'localhost:3009'
    VERIFY_WEBHOOK_MS = 'localhost:3006'
    VERIFY_EXPRESS_MS = 'localhost:3007'
else:
    SECRET_TOKEN = os.environ['SECRET_TOKEN']
    UTILITY_MS = os.environ['UTILITY_PATH']
    USER_MS = os.environ['USERS_PATH']
    EMAIL_MS = os.environ['EMAIL_PATH']
    BUCKET_MS = os.environ['BUCKET_PATH']
    VERIFY_WEBHOOK_MS = os.environ['VERIFY_WEBHOOK_PATH']
    VERIFY_EXPRESS_MS = os.environ['VERIFY_EXPRESS_PATH']

if 'TRUENATIVE_PATH' not in os.environ:
    TRUENATIVE_MS = 'localhost:4000'
else:
    TRUENATIVE_MS = os.environ['TRUENATIVE_PATH']

print(SECRET_TOKEN, flush=True)
print(UTILITY_MS, flush=True)
print(USER_MS, flush=True)
print(EMAIL_MS, flush=True)
print(BUCKET_MS, flush=True)
print(TRUENATIVE_MS, flush=True)
print(VERIFY_WEBHOOK_MS, flush=True)
print(VERIFY_EXPRESS_MS, flush=True)


if UTILITY_MS == 'utility':
    UTILITY_MS = 'utility:3004'
if USER_MS == 'users':
    USER_MS = 'users:3000'
if EMAIL_MS == 'send-email':
    EMAIL_MS = 'send-email:3008'
if BUCKET_MS == 'archive-email':
    BUCKET_MS = 'archive-email:3009'
if TRUENATIVE_MS == 'truenative':
    TRUENATIVE_MS = 'truenative:4000'
if VERIFY_WEBHOOK_MS == 'verify-webhook':
    VERIFY_WEBHOOK_MS = 'verify-webhook:3006'
if VERIFY_EXPRESS_MS == 'verify-express':
    VERIFY_EXPRESS_MS = 'verify-express:3007'

print(' * UTILITY_MS: {}'.format(UTILITY_MS), flush=True)
print(' * USER_MS: {}'.format(USER_MS), flush=True)
print(' * EMAIL_MS: {}'.format(EMAIL_MS), flush=True)
print(' * BUCKET_MS: {}'.format(BUCKET_MS), flush=True)
print(' * TRUENATIVE_MS: {}'.format(TRUENATIVE_MS), flush=True)
print(' * VERIFY_WEBHOOK_MS: {}'.format(VERIFY_WEBHOOK_MS), flush=True)
print(' * VERIFY_EXPRESS_MS: {}'.format(VERIFY_EXPRESS_MS), flush=True)


def enviarEmail(data):
    print('Enviando correo...', flush=True)
    url = 'http://{}/send_email'.format(EMAIL_MS)
    print(url)
    response = requests.post(url, json=data)
    return response.json(), response.status_code

def archiveEmail(data):
    url = 'http://{}/archive_email'.format(BUCKET_MS)
    print(url)
    response = requests.post(url, json=data)
    return response.json(), response.status_code

def processPubSub(body):
    print("Inicio del proceso de PubSub ----", flush=True)
    print(body, flush=True)
    publicador = ConcretePublicador()
    sub_archive = ConcreteArchiveEmail()
    sub_archive.executor = archiveEmail
    sub_archive.params = body
    publicador.attach(sub_archive)
    sub_email = ConcreteEnviarCorreo()
    sub_email.executor = enviarEmail
    sub_email.params = body
    publicador.attach(sub_email)
    # Almacenar Correo
    publicador.some_business_logic(1)
    time.sleep(2)
    # Enviar Correo
    publicador.some_business_logic(2)
    time.sleep(2)
    # Desuscribirse
    publicador.detach(sub_archive)
    publicador.detach(sub_email)
    print("Fin del proceso de PubSub ----", flush=True)

def fire_and_forget_pubsub(body):
    print(body)
    threading.Thread(target=processPubSub, args=(body,)).start()

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaPublicPost(Resource):
    def post(self):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        utility_ms_url = 'http://{}/public/posts'.format(UTILITY_MS)
        utility = requests.post(utility_ms_url, headers={'Authorization': auth_token}, json=request.json)
        return utility.json(), utility.status_code

class VistaPublicOffer(Resource):
    def post(self, id):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        utility_ms_url = 'http://{}/public/posts/{}/offers'.format(UTILITY_MS, id)
        utility = requests.post(utility_ms_url, headers={'Authorization': auth_token}, json=request.json)
        return utility.json(), utility.status_code

class VistaSearchPost(Resource):
    def get(self, id):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        utility_ms_url = 'http://{}/public/posts/{}'.format(UTILITY_MS, id)
        utility = requests.get(utility_ms_url, headers={'Authorization': auth_token})
        return utility.json(), utility.status_code

class VistaInfoUsuario(Resource):
    def get(self):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        return user.json(), user.status_code

class VistaGeneracionToken(Resource):
    def post(self):
        user_ms_url = 'http://{}/users/auth'.format(USER_MS)
        user = requests.post(user_ms_url, json=request.json)
        return user.json(), user.status_code

class VistaCrearUsuario(Resource):
    def post(self):
        user_ms_url = 'http://{}/users'.format(USER_MS)
        user = requests.post(user_ms_url, json=request.json)
        if(user.status_code == 201):
            user = user.json()
            validate_user_ms_url = 'http://{}/verify'.format(TRUENATIVE_MS) #aqui hay cambios apuntael trunateve
            body = {
                "user":{
                    'email':request.json.get('email', None),
                    'dni':request.json.get('dni', None),
                    'fullName':request.json.get('fullName', None),
                    'phone':request.json.get('phone', None)
                    },
                "transactionIdentifier": str(uuid.uuid1()),
                "userIdentifier": str(user['id']),
                "userWebhook": "http://{}/webhook".format(VERIFY_WEBHOOK_MS),
            }
            validate_user = requests.post(validate_user_ms_url, headers={'Authorization': 'Bearer ' + SECRET_TOKEN}, json=body)
            if (validate_user.status_code != 201):
                return validate_user.json(), validate_user.status_code
            validate_user = validate_user.json()
            verify_express_ms_url = 'http://{}/addTask'.format(VERIFY_EXPRESS_MS)
            body = {
                "RUV":validate_user['RUV'],
            }
            verify_express = requests.post(verify_express_ms_url, json=body)
            return verify_express.json(), verify_express.status_code
        else:
            return user.json(), user.status_code

class VistaManual(Resource):
    def post(self):
        email = request.json.get('email', None)
        if email is None:
            return {'error': 'Faltan datos en la solicitud.'}, 400
        
        user_ms_url = 'http://{}/user_base'.format(USER_MS)
        bodyUser ={
            "email":email
        }
        user = requests.post(user_ms_url, json=bodyUser)
        user_data = user.json()
        print(user_data,flush=True)
        if(user.status_code != 200):
            return user.json(), user.status_code
        
        if( user_data['status'] == "VERIFICADO"):
            return {'error': 'El usuario ya está verificado con un puntaje superior o igual a 80.'}, 409

        validate_user_ms_url = 'http://{}/verify'.format(TRUENATIVE_MS) #aqui hay cambios apuntael trunateve
        body_validate = {
            "user":{
                'email':email,
                },
            "transactionIdentifier": str(uuid.uuid1()),
            "userIdentifier": str(user_data['id']),
            "userWebhook": "http://{}/webhook".format(VERIFY_WEBHOOK_MS),
        }
        validate_user = requests.post(validate_user_ms_url, headers={'Authorization': 'Bearer ' + SECRET_TOKEN}, json=body_validate)
        if (validate_user.status_code != 201):
            return validate_user.json(), validate_user.status_code
        validate_user = validate_user.json()
        verify_express_ms_url = 'http://{}/addTask'.format(VERIFY_EXPRESS_MS)
        body_express = {
            "RUV":validate_user['RUV'],
        }
        print(body_express,flush=True)
        print(verify_express_ms_url,flush=True)
        verify_express = requests.post(verify_express_ms_url, json=body_express)
        return verify_express.json(), verify_express.status_code
        

class VistaPubSubUser(Resource):
    def post(self):
        receiver = request.json.get('receiver', None)
        subject = request.json.get('subject', None)
        body_mail = request.json.get('body_mail', None)
        if receiver is None or subject is None or body_mail is None:
            return {'error': 'Faltan datos en la solicitud.'}, 400
        
        body = {
            'receiver':receiver,
            'subject':subject,
            'body_mail':body_mail
        }

        fire_and_forget_pubsub(body)
        return {'message': 'Proceso de archivo y envio de correo empezado'}, 200


class VistaInfoBaseUser(Resource):
    def post(self):
        email = request.json.get('email', None)
        if email is None:
            return {'error': 'Faltan datos en la solicitud.'}, 400
        
        user_ms_url = 'http://{}/user_base'.format(USER_MS)
        bodyUser ={
            "email":email
        }
        user = requests.post(user_ms_url, json=bodyUser)
        return user.json(), user.status_code