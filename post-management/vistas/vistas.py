from modelos.modelos import ( Publicacion, PublicacionSchema, db)
from datetime import datetime, timedelta
import hashlib
import os
import json
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from dateutil.parser import parse


if 'USERS_PATH' not in os.environ:
    USER_MS = 'localhost:3000'
else:
    USER_MS = os.environ['USERS_PATH']


if 'ISLOCALG14' not in os.environ:
    ISLOCALG14 = False
else:
    ISLOCALG14 = os.environ['ISLOCALG14']

if USER_MS == 'users' and ISLOCALG14 == False:
    USER_MS = 'users:3000'
    
if USER_MS is None or USER_MS == '' or USER_MS == 'users':
    USER_MS = 'host.docker.internal:3000'

print('USER_MS:',USER_MS)
prulicaciono_schema = PublicacionSchema()
def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaConsultarPublicacion(Resource):
    def get(self, id_publicacion):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        user_info = user.json()
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        
        if not id_publicacion.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_publicacion = int(id_publicacion)
        publicacion_buscado = Publicacion.query.filter_by(id=int(id_publicacion)).first()

        if not publicacion_buscado:
            return {'error': 'No existe la publicacion con ese identificador..'}, 404
        else:
            return {'id': publicacion_buscado.id, 
                    'routeId':str(publicacion_buscado.routeId), 
                    'userId': publicacion_buscado.userId, 
                    'plannedStartDate': str(publicacion_buscado.plannedStartDate), 
                    'plannedEndDate': str(publicacion_buscado.plannedEndDate), 
                    'createdAt': str(publicacion_buscado.createdAt)} , 200
    
    def put(self, id_publicacion):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        user_info = user.json()
        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        else:
            id_user = user_info["id"]
        
        if not id_publicacion.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_publicacion = int(id_publicacion)
        
        publicacion_buscado = Publicacion.query.filter_by(id=int(id_publicacion)).first()
    
        if not publicacion_buscado:
            return {'error': 'No existe la publicacion con ese identificador..'}, 404
        else:
            parser = reqparse.RequestParser() 
            parser.add_argument('routeId', required=False)
            parser.add_argument('plannedStartDate', required=False)
            parser.add_argument('plannedEndDate', required=False)
            args = parser.parse_args()
            routeId = args['routeId']
            plannedStartDate = args['plannedStartDate']
            plannedEndDate = args['plannedEndDate']
            if not routeId.isnumeric():
                return {'error': 'El campo no es numerico.'}, 400
            else:
                routeId = int(routeId)
            if is_date(plannedStartDate) == False:
                return {'error': 'La fecha no tiene el formato correcto.'}, 400
            if is_date(plannedEndDate) == False:
                return {'error': 'La fecha no tiene el formato correcto.'}, 400
            if parse(plannedStartDate) > parse(plannedEndDate):
                return {'error': 'La fecha de inicio no puede ser mayor a la fecha final.'}, 400
            if id_user != None:
                publicacion_buscado.userId = id_user
            if routeId != None:
                publicacion_buscado.routeId = routeId
            if plannedStartDate != None:
                publicacion_buscado.plannedStartDate = datetime.strptime(plannedStartDate, '%Y-%m-%d %H:%M:%S')
            if plannedEndDate != None:
                publicacion_buscado.plannedEndDate = datetime.strptime(plannedEndDate, '%Y-%m-%d %H:%M:%S')
            db.session.commit()
            return {'id': publicacion_buscado.id, 
                    'routeId':str(publicacion_buscado.routeId), 
                    'userId': publicacion_buscado.userId, 
                    'plannedStartDate': str(publicacion_buscado.plannedStartDate), 
                    'plannedEndDate': str(publicacion_buscado.plannedEndDate), 
                    'createdAt': str(publicacion_buscado.createdAt)} , 200
    
    def delete(self, id_publicacion):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})

        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401

        if not id_publicacion.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_publicacion = int(id_publicacion)
        
        publicacion_buscado = Publicacion.query.filter_by(id=int(id_publicacion)).first()
    
        if not publicacion_buscado:
            return {'error': 'No existe la publicacion con ese identificador..'}, 404
        else:
            db.session.delete(publicacion_buscado)
            db.session.commit()
            return {'message': 'publicacion eliminada'}, 200
                
class VistaBuscarPublicacion(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser() 
            parser.add_argument('when', required=False)
            parser.add_argument('route', required=False)
            parser.add_argument('filter', required=False)
            args = parser.parse_args()
            when = args['when']
            route = args['route']
            filter = args['filter']
        except:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        user_info = user.json()

        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        else:
            id_user = user_info["id"]
        
        if not when or not route or not filter:
            publicacion_buscado = Publicacion.query.all()
        else:
            if not route.isnumeric():
                return {'error': 'El campo no es numerico.'}, 400
            else:
                route = int(route)
            if is_date(when) == False:
                return {'error': 'La fecha no tiene el formato correcto.'}, 400
            if when == None or route == None or filter == None:
                return {'error': 'Alguno de los campos no estan presentes en la solicitud o el formato no es correcto.'}, 400
            
            if filter == 'me':
                publicacion_buscado = Publicacion.query.filter_by(routeId=route, userId=id_user).all()
            else:
                publicacion_buscado = Publicacion.query.filter_by(routeId=route).all()

            publicacion_buscado_ = [t for t in publicacion_buscado if (parse(when) >= (t.plannedStartDate) and parse(when) <= (t.plannedEndDate))]
            publicacion_buscado = publicacion_buscado_

        if not publicacion_buscado:
            return {'error': 'no se encontraron publicaciones con esas caracteristicas'}, 200
        
        publicaciones = []
        for publicacion in publicacion_buscado:
            publicaciones.append({
                                'id': publicacion.id, 
                                "routeId": publicacion.routeId, 
                                "userId": publicacion.userId,
                                "plannedStartDate": str(publicacion.plannedStartDate),
                                "plannedEndDate": str(publicacion.plannedEndDate), 
                                "createdAt": str(publicacion.createdAt)})

        return publicaciones, 200

class VistaCrearPublicacion(Resource):
    def post(self):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        user_info = user.json()

        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        else:
            id_user = user_info["id"]
        try:
            routeId = request.json["routeId"]
            plannedStartDate = request.json['plannedStartDate']
            plannedEndDate = request.json['plannedEndDate']
        except:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        if not routeId or not plannedStartDate or not plannedEndDate:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        if is_date(plannedStartDate) == False or is_date(plannedEndDate) == False:
            return {'error': 'La fecha no tiene el formato correcto.'}, 412

        plannedStartDate = parse(plannedStartDate)  #datetime.strptime(plannedStartDate, '%Y-%m-%d').date()
        plannedEndDate = parse(plannedEndDate) #datetime.strptime(plannedEndDate, '%Y-%m-%d').date()

        if plannedStartDate > plannedEndDate:
            return {'error': 'La fecha de inicio no puede ser menor a la fecha final.'}, 412
        
        createdAt = datetime.now()
        publicacion = Publicacion(routeId=routeId, userId=id_user, plannedStartDate=plannedStartDate, plannedEndDate=plannedEndDate, createdAt= createdAt)
    
        db.session.add(publicacion)
        db.session.commit()
        return {'id': publicacion.id, 'userId': id_user, 'createdAt': str(createdAt)}, 201