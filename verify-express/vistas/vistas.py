from datetime import datetime, timedelta
import hashlib
import os
import requests
from flask import request
from flask_restful import Resource, reqparse
from dateutil.parser import parse
import json
import uuid
import queue
import multiprocessing
import time

SECRET_TOKEN = ''
TRUENATIVE_MS = ''
USER_MS = ''
SIDECARAPI_MS = ''

if 'SECRET_TOKEN' not in os.environ:
    SECRET_TOKEN = 'gcloudprojectg14'
    USER_MS = 'localhost:3000'
    SIDECARAPI_MS = 'localhost:3005'
else:
    SECRET_TOKEN = os.environ['SECRET_TOKEN']
    USER_MS = os.environ['USERS_PATH']
    SIDECARAPI_MS = os.environ['SIDECARAPI_PATH']

if 'TRUENATIVE_PATH' not in os.environ:
    TRUENATIVE_MS = 'localhost:4000'
else:
    TRUENATIVE_MS = os.environ['TRUENATIVE_PATH']

print(SECRET_TOKEN, flush=True)
print(TRUENATIVE_MS, flush=True)
print(USER_MS, flush=True)
print(SIDECARAPI_MS, flush=True)

if TRUENATIVE_MS == 'truenative':
    TRUENATIVE_MS = 'truenative:4000'
if USER_MS == 'users':
    USER_MS = 'users:3000'
if SIDECARAPI_MS == 'sidecarapi':
    SIDECARAPI_MS = 'sidecarapi:3005'

print(' * TRUENATIVE_MS: {}'.format(TRUENATIVE_MS), flush=True)
print(' * USER_MS: {}'.format(USER_MS), flush=True)
print(' * SIDECARAPI_MS: {}'.format(SIDECARAPI_MS), flush=True)

AUTH_TOKEN = 'Bearer ' + SECRET_TOKEN


task_queue = multiprocessing.Queue()
process:multiprocessing.Process = None

def cola_express(task_queue):
    while True:
        try:
            task_id, executor = task_queue.get(timeout=1)
            result = executor(task_id)
            if not result:
                task_queue.put((task_id, executor))
            time.sleep(2)
        except queue.Empty:
            break

def encolar_tarea(task_id:str, executor: any) -> None:
    task_queue.put((task_id, executor))
    global process

    if process is None or not process.is_alive():
        process = multiprocessing.Process(target=cola_express, args=(task_queue,))
        process.start()

def process_task(ruv: str) -> bool:
    try:
        verify_ruv_url = 'http://{}/verify/{}'.format(TRUENATIVE_MS, ruv)
        verify_ruv = requests.get(verify_ruv_url, headers={'Authorization': AUTH_TOKEN})

        if verify_ruv.status_code != 200:
            return False
        
        data = verify_ruv.json()
        print(data)
        if data["status"] == "PENDING":
            return True
        elif data["status"] == "DELIVERED":
            return True
        if data["status"] == "ACCEPTED":
            return False
        
        email = ''
        status = ''
        
        if data["score"] != None:
            if data["score"] >= 80:
                status = "VERIFICADO"
                print('-----------------------------------------------')
                print ('Score mayor o igual a 80')
                print('-----------------------------------------------')                
            else:
                status = "NO_VERIFICADO"
                print('-----------------------------------------------')
                print ('Score menor a 80')
                print('-----------------------------------------------')
            user_confirmed_ms_url = 'http://{}/users'.format(USER_MS)
            body_user_confirmed = {
                "id": data['userIdentifier'],
                "status": status
            }
            print(user_confirmed_ms_url, flush=True)
            user_confirmed = requests.put(user_confirmed_ms_url, json=body_user_confirmed)
            if user_confirmed.status_code != 201:
                return False
            data_user = user_confirmed.json()
            email = data_user['email'] 
            print(email, flush=True) 
            if email != '':
                pubsubuser_url = 'http://{}/pubsubuser'.format(SIDECARAPI_MS)
                bodyPubSub = {
                    "receiver": email,
                    "subject": "Verificación de identidad",
                    "body_mail": "Su verificación de identidad ha sido completada ["+ str(status) +"]. \nSu puntaje es: " + str(data["score"]) + ".\n"
                }
                pubsubuser = requests.post(pubsubuser_url, json=bodyPubSub)
                if pubsubuser.status_code != 200:
                    return False
            return True
        else:
            return False
    except Exception as err:
        print("Error processing task %s: %s" % (ruv, err))
        return True


class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaAgregarCola(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        RUV = data['RUV']
        encolar_tarea(RUV, process_task)
        return 'ok', 200