from modelos.modelos import ( Trayecto, TrayectoSchema, db)
from datetime import datetime, timedelta
import hashlib
import os
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from dateutil.parser import parse

#USER_MS = config('USER_MS')
#USER_MS = 'localhost:5000'
# Si USERS_PATH no está en las variables de entorno, se usa localhost:3000, sino se usa el valor de USERS_PATH
if 'USERS_PATH' not in os.environ:
    USER_MS = 'localhost:3000'
else:
    USER_MS = os.environ['USERS_PATH']

# Si ISLOCALG14 no está en las variables de entorno, se usa False, sino se usa el valor de ISLOCALG14
if 'ISLOCALG14' not in os.environ:
    ISLOCALG14 = False
else:
    ISLOCALG14 = os.environ['ISLOCALG14']

# Si ISLOCALG14 es False y USER_MS es users, se usa users:3000, sino se usa el valor de USER_MS
if USER_MS == 'users' and ISLOCALG14 == False:
    USER_MS = 'users:3000'
    
if USER_MS is None or USER_MS == '' or USER_MS == 'users':
    USER_MS = 'host.docker.internal:3000'

print('USER_MS:',USER_MS)
trayecto_schema = TrayectoSchema()
def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaManejarTrayecto(Resource):
    def get(self, id_trayecto):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        
        if not id_trayecto.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_trayecto = int(id_trayecto)
        
        trayecto_buscado = Trayecto.query.filter_by(id=int(id_trayecto)).first()
    
        if not trayecto_buscado:
            return {'error': 'No existe el trayecto con ese identificador..'}, 404
        else:
            print("trayecto::: ", trayecto_buscado)
            return {'id': trayecto_buscado.id, 
                    'sourceAirportCode':str(trayecto_buscado.sourceAirportCode), 
                    'sourceCountry': trayecto_buscado.sourceCountry, 
                    'destinyAirportCode': trayecto_buscado.destinyAirportCode, 
                    'destinyCountry': trayecto_buscado.destinyCountry, 
                    'bagCost': trayecto_buscado.bagCost,
                    'createdAt': str(trayecto_buscado.createdAt),
                    'expireAt': str(trayecto_buscado.createdAt + timedelta(days=30))
                    } , 200
    
    def put(self, id_trayecto):
        sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost = None, None, None, None, None
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        try:
            sourceAirportCode = request.json["sourceAirportCode"]
            sourceCountry = request.json['sourceCountry']
            destinyAirportCode = request.json['destinyAirportCode']
            destinyCountry = request.json["destinyCountry"]
            bagCost = request.json["bagCost"]
            
        except:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400

        if not id_trayecto.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_trayecto = int(id_trayecto)
        
        trayecto_buscado = Trayecto.query.filter_by(id=int(id_trayecto)).first()

        if not trayecto_buscado:
            return {'error': 'el trayecto no existe'}, 404

        if sourceAirportCode != None:
            trayecto_buscado.sourceAirportCode = sourceAirportCode
        if sourceCountry != None:
            trayecto_buscado.sourceCountry = sourceCountry
        if destinyAirportCode != None:
            trayecto_buscado.destinyAirportCode = destinyAirportCode
        if destinyCountry != None:
            trayecto_buscado.destinyCountry = destinyCountry
        if bagCost != None:
            trayecto_buscado.bagCost = bagCost
        
        db.session.commit()
        return {
            'id': trayecto_buscado.id, 
            'sourceAirportCode': trayecto_buscado.sourceAirportCode, 
            'sourceCountry': trayecto_buscado.sourceCountry, 
            'destinyAirportCode': trayecto_buscado.destinyAirportCode, 
            'destinyCountry': trayecto_buscado.destinyCountry, 
            'bagCost': trayecto_buscado.bagCost,
            'createdAt': str(trayecto_buscado.createdAt),
            'expireAt': str(trayecto_buscado.createdAt + timedelta(days=30))
        }, 200

    def delete(self, id_trayecto):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401

        if not id_trayecto.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_trayecto = int(id_trayecto)
        
        trayecto_buscado = Trayecto.query.filter_by(id=int(id_trayecto)).first()

        if not trayecto_buscado:
            return {'error': 'el trayecto no existe'}, 404
        
        db.session.delete(trayecto_buscado)
        db.session.commit()
        return {'message': 'trayecto eliminado'}, 200

class VistaBuscarTrayecto(Resource):
    def get(self):
        desde, hasta, fecha = None, None, None
        try:
            parser = reqparse.RequestParser() 
            parser.add_argument('from', required=False)
            parser.add_argument('to', required=False)
            parser.add_argument('when', required=False)
            args = parser.parse_args()
            desde = args['from']
            hasta = args['to']
            fecha = args['when']
        except:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        # verificar que los datos no esten vacios
        if not desde or not hasta or not fecha:
            #return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
            trayectos_buscados = Trayecto.query.all()
        else:
            if is_date(fecha) == False:
                return {'error': 'La fecha no tiene el formato correcto.'}, 400
            trayectos_buscados = Trayecto.query.filter_by(sourceAirportCode=desde, destinyAirportCode=hasta).all()
            trayectos_buscados_ = [t for t in trayectos_buscados if (t.createdAt + timedelta(days=30)) >= parse(fecha)]
            trayectos_buscados = trayectos_buscados_
        if not trayectos_buscados:
            return {'error': 'no se encontraron trayectos con esas caracteristicas'}, 200
        else:
            trayectos = []
            for trayecto in trayectos_buscados:
                trayectos.append({
                    'id': trayecto.id, 
                    "sourceAirportCode": trayecto.sourceAirportCode,
                    "sourceCountry": trayecto.sourceCountry,
                    "destinyAirportCode": trayecto.destinyAirportCode,
                    "destinyCountry": trayecto.destinyCountry,
                    "bagCost": trayecto.bagCost,
                    'createdAt': str(trayecto.createdAt),
                    'expireAt': str(trayecto.createdAt + timedelta(days=30))
                })
            return trayectos, 200

class VistaCrearTrayecto(Resource):
    def post(self):
        sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost = None, None, None, None, None
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401

        try:
            sourceAirportCode = request.json["sourceAirportCode"]
            sourceCountry = request.json['sourceCountry']
            destinyAirportCode = request.json['destinyAirportCode']
            destinyCountry = request.json["destinyCountry"]
            bagCost = request.json["bagCost"]
            
        except:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        now = datetime.now()
        # verificar que los datos no esten vacios
        if not sourceAirportCode or not sourceCountry or not destinyAirportCode or not destinyCountry or not bagCost:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        
        if Trayecto.query.filter_by(sourceAirportCode=sourceAirportCode, destinyAirportCode=destinyAirportCode).first():
            return {'error': 'el trayecto con los aeropuertos de inicio y de destino ya existe'}, 412
        bagCost = int(bagCost)
        createdAt = datetime.now()
        expireAt = now + timedelta(days=30)
        trayecto = Trayecto(sourceAirportCode=sourceAirportCode, sourceCountry=sourceCountry, destinyAirportCode=destinyAirportCode, destinyCountry= destinyCountry, bagCost=bagCost, createdAt= createdAt)
    
        db.session.add(trayecto)
        db.session.commit()
        return {'id': trayecto.id, 'createdAt': str(trayecto.createdAt), 'expireAt': str(expireAt)}, 201