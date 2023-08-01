from modelos.modelos import ( Oferta, OfertaSchema, db)
from datetime import datetime, timedelta
import hashlib
import os
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from flask_restx import inputs

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
oferta_schema = OfertaSchema()


class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaConsultarOferta(Resource):
    def get(self, id_oferta):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})

        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        
        if not id_oferta.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_oferta = int(id_oferta)
        
        oferta_buscada = Oferta.query.filter_by(id=id_oferta).first()
        print(oferta_buscada)
        if not oferta_buscada:
            return {'error': 'No existe la oferta con ese identificador..'}, 404
        else:
            return {'id': oferta_buscada.id, 
                    'postId':str(oferta_buscada.postId), 
                    'userId': oferta_buscada.userId, 
                    'description': oferta_buscada.description, 
                    'size': oferta_buscada.size, 
                    'fragile': oferta_buscada.fragile,
                    "offer": oferta_buscada.offer,
                    "createdAt": str(oferta_buscada.createdAt)} , 200
    
    def put(self, id_oferta):
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
        if not id_oferta.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_oferta = int(id_oferta)
        oferta_buscada = Oferta.query.filter_by(id=id_oferta).first()
        if not oferta_buscada:
            return {'error': 'No existe la oferta con ese identificador..'}, 404
        else:
            parser = reqparse.RequestParser() 
            parser.add_argument('postId', required=False)
            parser.add_argument('description', required=False)
            parser.add_argument('size', required=False)
            parser.add_argument('fragile', required=False, type=inputs.boolean)
            parser.add_argument('offer', required=False)
            args = parser.parse_args()
            postId = args['postId']
            description = args['description']
            size = args['size']
            fragile = args['fragile']
            offer = args['offer']
            if id_user != None:
                oferta_buscada.userId = id_user
            if postId != None:
                oferta_buscada.postId = postId
            if description != None:
                oferta_buscada.description = description
            if size != None:
                oferta_buscada.size = size
            if fragile != None:
                oferta_buscada.fragile = fragile
            if offer != None:
                oferta_buscada.offer = offer
            db.session.commit()
            return {'id': oferta_buscada.id,
                    'postId':str(oferta_buscada.postId), 
                    'userId': oferta_buscada.userId, 
                    'description': oferta_buscada.description, 
                    'size': oferta_buscada.size, 
                    'fragile': oferta_buscada.fragile,
                    "offer": oferta_buscada.offer,
                    "createdAt": str(oferta_buscada.createdAt)} , 200
    
    def delete(self, id_oferta):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})

        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        if not id_oferta.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            id_oferta = int(id_oferta)
        oferta_buscada = Oferta.query.filter_by(id=id_oferta).first()
        if not oferta_buscada:
            return {'error': 'No existe la oferta con ese identificador..'}, 404
        else:
            db.session.delete(oferta_buscada)
            db.session.commit()
            return {'message': 'Oferta eliminada correctamente.'}, 200

class VistaBuscarListarOferta(Resource):
    #def get(self, post, filter):
    def get(self):
        post, filter = None, None
        try:
            parser = reqparse.RequestParser() 
            parser.add_argument('post', required=True)
            parser.add_argument('filter', required=True)
            args = parser.parse_args()
            post = args['post']
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

        if not post.isnumeric():
            return {'error': 'El campo no es numerico.'}, 400
        else:
            post = int(post)
        # verificar que los datos no esten vacios
        if post == None or not (filter=='me') or filter == None:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud o el formato no es correcto.'}, 400
        ofertas = []
        ofertas_buscados = Oferta.query.filter_by(postId=post, userId=id_user).all()
        if not ofertas_buscados:
            return {'error': 'No existe las ofertas con estas caracteristicas.'}, 404
        for oferta in ofertas_buscados:
            ofertas.append({'id': oferta.id, 
                            "postId": oferta.postId, 
                            "userId": oferta.userId,
                            "description": oferta.description,
                            "size": oferta.size, 
                            "offer": oferta.offer,
                            "createdAt": str(oferta.createdAt)})

            return ofertas, 200

class VistaCrearOferta(Resource):
    def post(self):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        try:
            postId = request.json["postId"]
            description = request.json['description']
            size = request.json['size']
            fragile = request.json['fragile']
            offer = request.json['offer']
            auth_token = request.headers['Authorization']
        except:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        # verificar que los datos no esten vacios
        print(postId, description, size, fragile, offer)
        if postId == None or description  == None or size == None or fragile  == None or offer == None:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        
        if (size not in ("LARGE", "MEDIUM","SMALL")) or offer <= 0: 
            return {'error': 'el campo size no es valido o la oferta es menor o igual a cero.'}, 412

        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        user_info = user.json()

        if user.status_code == 401:
            return {'error':'El token no es válido o está vencido.'}, 401
        else:
            id_user = user_info["id"]
        
        createdAt = datetime.now()
        oferta = Oferta(postId=postId, userId=id_user, description=description, size=size, fragile=fragile, offer=offer, createdAt=createdAt)
    
        db.session.add(oferta)
        db.session.commit()
        return {'id': oferta.id, 'userId': id_user, 'createdAt': str(createdAt)}, 201