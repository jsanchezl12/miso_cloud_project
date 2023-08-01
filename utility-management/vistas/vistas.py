from modelos.modelos import ( Utilidad, UtilidadSchema, db)
from datetime import datetime, timedelta
import os
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from dateutil.parser import parse
import json
import hashlib


if 'USERS_PATH' not in os.environ:
    USER_MS = 'localhost:3000'
    POST_MS = 'localhost:3001'
    ROUTE_MS = 'localhost:3002'
    OFFER_MS = 'localhost:3003'

else:
    USER_MS = os.environ['USERS_PATH']
    POST_MS = os.environ['POSTS_PATH']
    ROUTE_MS = os.environ['ROUTES_PATH']
    OFFER_MS = os.environ['OFFERS_PATH']

if 'ISLOCALG14' not in os.environ:
    ISLOCALG14 = False
else:
    ISLOCALG14 = os.environ['ISLOCALG14']

if USER_MS == 'users':
    USER_MS = 'users:3000'
    POST_MS = 'posts:3001'
    ROUTE_MS = 'routes:3002'
    OFFER_MS = 'offers:3003'


print(' * USER_MS: {}'.format(USER_MS), flush=True)
print(' * POST_MS: {}'.format(POST_MS), flush=True)
print(' * ROUTE_MS: {}'.format(ROUTE_MS), flush=True)
print(' * OFFER_MS: {}'.format(OFFER_MS), flush=True)

utilidad_schema = UtilidadSchema()

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaPublicPost(Resource):
    def post(self):

        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        plannedStartDate = request.json.get('plannedStartDate', None)
        plannedEndDate = request.json.get('plannedEndDate', None)
        origin = request.json.get('origin', None)
        destiny = request.json.get('destiny', None)
        bagCost = request.json.get('bagCost', None) 
        if not origin or not destiny:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        originAirportCode = origin['airportCode']
        originCountry = origin['country']
        destinyAirportCode = destiny['airportCode']
        destinyCountry = destiny['country']

        if ( not plannedStartDate or not plannedEndDate or not origin or not destiny or not bagCost 
            or not originAirportCode or not originCountry or not destinyAirportCode or not destinyCountry ):
                return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error': 'El token no es válido o está vencido.'}, 401
        if parse(plannedEndDate) < parse(plannedStartDate):
            return {'error': 'Las fechas no son válidas'}, 412
        if parse(plannedStartDate) < datetime.now():
            return {'error': 'Las fechas no son válidas'}, 412
        if parse(plannedEndDate) < datetime.now():
            return {'error': 'Las fechas no son válidas'}, 412
        if parse(plannedStartDate) > datetime.now() + timedelta(days=30):
            return {'error': 'Las fechas no son válidas'}, 412
        
        base_user = json.loads(user.content.decode('utf-8'))
        route_ms_url = 'http://{}/routes?from={}&to={}&when={}'.format(
            ROUTE_MS, originAirportCode, destinyAirportCode, plannedStartDate)
        routes = requests.get(route_ms_url, headers={
                            'Authorization': auth_token})
        
        if routes.status_code == 200:
            if routes.content.__contains__(b'no se encontraron trayectos'):
                route_create_url = 'http://{}/routes/'.format(ROUTE_MS)
                route_create = requests.post(route_create_url, headers={'Authorization': auth_token},
                                            json={
                                                'sourceAirportCode': originAirportCode,
                                                'sourceCountry': originCountry,
                                                'destinyAirportCode': destinyAirportCode,
                                                'destinyCountry': destinyCountry,
                                                'bagCost': int(bagCost)})
                if route_create.status_code == 201:
                    base_route = json.loads(route_create.content.decode('utf-8'))
                    post_create_url = 'http://{}/posts/'.format(POST_MS)
                    post_create = requests.post(post_create_url, headers={'Authorization': auth_token},
                                                    json={
                                                        'routeId': base_route['id'],
                                                        'plannedStartDate': plannedStartDate,
                                                        'plannedEndDate': plannedEndDate
                                                    })
                    if post_create.status_code == 201:
                        base_publication = json.loads(post_create.content.decode('utf-8'))
                        return {
                            "data": {
                                "id": base_publication['id'], #id de la publicación,
                                "userId": base_user['id'] ,#id del usuario que crea la publicación,
                                "createdAt": base_publication['createdAt'],#fecha de creación de la publicación en formato ISO,
                                "route" : {
                                    "id": base_route['id'] , #id del trayecto,
                                    "createdAt": base_route['createdAt'] , #fecha de creación del trayecto en formato ISO,
                                    "expireAt": base_route['expireAt'] #último día de validez del trayecto en formato ISO.
                                }
                            },
                            "msg": "Ruta y Publicación creada con éxito."
                        }, 200
                    else:
                        route_delete_url = 'http://{}/routes/{}'.format(ROUTE_MS, base_route['id'])
                        requests.delete(route_delete_url, headers={'Authorization': auth_token})
                        return json.loads(post_create.content.decode('utf-8')), 400
                else:
                    return json.loads(route_create.content.decode('utf-8')), 400
            else:
                if len(json.loads(routes.content.decode('utf-8'))) > 0:
                    base_route = json.loads(routes.content.decode('utf-8'))[0]
                    post_ms_url = 'http://{}/posts?when={}&route={}&filter=me'.format(
                        POST_MS, plannedStartDate, base_route['id'])
                    posts = requests.get(post_ms_url, headers={
                        'Authorization': auth_token})
                    if posts.status_code == 200:

                        if posts.content.__contains__(b'no se encontraron publicaciones'):
                            post_create_url = 'http://{}/posts/'.format(POST_MS)
                            post_create = requests.post(post_create_url, headers={'Authorization': auth_token},
                                                            json={
                                                                'routeId': base_route['id'],
                                                                'plannedStartDate': plannedStartDate,
                                                                'plannedEndDate': plannedEndDate
                                                            })
                            if post_create.status_code == 201:
                                base_publication = json.loads(post_create.content.decode('utf-8'))
                                return {
                                    "data": {
                                        "id": base_publication['id'], #id de la publicación,
                                        "userId": base_user['id'] ,#id del usuario que crea la publicación,
                                        "createdAt": base_publication['createdAt'],#fecha de creación de la publicación en formato ISO,
                                        "route" : {
                                            "id": base_route['id'] , #id del trayecto,
                                            "createdAt": base_route['createdAt'] , #fecha de creación del trayecto en formato ISO,
                                            "expireAt": base_route['expireAt'] #último día de validez del trayecto en formato ISO.
                                        }
                                    },
                                    "msg": "Ruta asociada y Publicación creada con éxito."
                                }, 200
                            else:
                                return json.loads(post_create.content.decode('utf-8')), 400
                        else:
                            if len(json.loads(posts.content.decode('utf-8'))) > 0:
                                base_publication = json.loads(posts.content.decode('utf-8'))[0]
                                if base_publication['routeId'] == base_route['id'] and parse(base_publication['plannedStartDate']) == parse(plannedStartDate) and parse(base_publication['plannedEndDate']) == parse(plannedEndDate):
                                    return {'error': 'Ya existe una publicación con los mismos datos'}, 412
                                print(base_publication)
                                post_update_url = 'http://{}/posts/{}'.format(POST_MS, base_publication['id'])
                                post_update = requests.put(post_update_url, headers={'Authorization': auth_token},
                                                                json={
                                                                    'routeId': base_route['id'],
                                                                    'plannedStartDate': plannedStartDate,
                                                                    'plannedEndDate': plannedEndDate
                                                                })
                                if post_update.status_code == 200:
                                    base_publication = json.loads(
                                        post_update.content.decode('utf-8'))
                                    return {
                                        "data": {
                                            "id": base_publication['id'], #id de la publicación,
                                            "userId": base_user['id'] ,#id del usuario que crea la publicación,
                                            "createdAt": base_publication['createdAt'],#fecha de creación de la publicación en formato ISO,
                                            "route" : {
                                                "id": base_route['id'] , #id del trayecto,
                                                "createdAt": base_route['createdAt'] , #fecha de creación del trayecto en formato ISO,
                                                "expireAt": base_route['expireAt'] #último día de validez del trayecto en formato ISO.
                                            }
                                        },
                                        "msg": "Ruta asociada y Publicación actualizada con éxito."
                                    }, 200
                                else:
                                    return json.loads(post_update.content.decode('utf-8')), 400
                    else:
                        return json.loads(posts.content.decode('utf-8')), posts.status_code
        else:
            return json.loads(routes.content.decode('utf-8')), routes.status_code

class VistaPublicOffer(Resource):
    def post(self, id):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        
        description = request.json.get('description', None)
        size = request.json.get('size', None)
        fragile = request.json.get('fragile', None)
        offer = request.json.get('offer', None)

        if not description or not size or not fragile or not offer or not id:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        
        if user.status_code == 401:
            return {'error': 'El token no es válido o está vencido.'}, 401
        post_ms_url = 'http://{}/posts/{}'.format(POST_MS, id)
        post = requests.get(post_ms_url, headers={'Authorization': auth_token})
        if post.status_code == 200:
            base_post = json.loads(post.content.decode('utf-8'))
            if base_post['userId'] == json.loads(user.content.decode('utf-8'))['id']:
                return {'error': 'No se puede hacer una oferta a una publicación propia.'}, 412
            route_ms_url = 'http://{}/routes/{}'.format(ROUTE_MS, base_post['routeId'])
            route = requests.get(route_ms_url, headers={'Authorization': auth_token})
            if route.status_code == 200:
                base_route = json.loads(route.content.decode('utf-8'))
                bagCost = base_route['bagCost']
                percentage_bag = 1 if (size == "LARGE") else 0.5 if (size == "MEDIUM") else 0.25 if (size == "SMALL") else 0
                utility_score = int(offer) - (percentage_bag * int(bagCost))
                offer_ms_url = 'http://{}/offers'.format(OFFER_MS)
                offer_create = requests.post(offer_ms_url, headers={'Authorization': auth_token},
                                                json={
                                                    'description': description,
                                                    'size': size,
                                                    'fragile': bool(fragile),
                                                    'offer': int(offer),
                                                    'postId': id
                                                })
                if offer_create.status_code == 201:
                    base_offer = json.loads(offer_create.content.decode('utf-8'))
                    print(base_offer['id'], base_offer['userId'], base_post['routeId'], base_post['id'], utility_score)
                    utilidad_entity = Utilidad(idUsuario=base_offer['userId'], idOferta=base_offer['id'], idTrayecto=base_post['routeId'],idPost=base_post['id'], utilidadOferta=utility_score)
                    db.session.add(utilidad_entity)
                    db.session.commit()
                    return {
                            "data": {
                                "id": base_offer['id'] ,#id de la oferta,
                                "userId": base_offer['userId'] ,# id del usuario dueño de la oferta,
                                "createdAt": base_offer['createdAt'], #fecha de creación de la oferta,
                                "postId": id, # id de la publicación
                            },
                        "msg": "Oferta creada con éxito."
                    }, 200
                else:
                    return json.loads(offer_create.content.decode('utf-8')), 404  
            else:
                return json.loads(route.content.decode('utf-8')), 404
        else:
            return json.loads(post.content.decode('utf-8')), post.status_code

class VistaSearchPost(Resource):
    def get(self, id):
        if 'Authorization' not in request.headers:
            return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
        auth_token = request.headers['Authorization']
        user_ms_url = 'http://{}/users/me'.format(USER_MS)
        user = requests.get(user_ms_url, headers={'Authorization': auth_token})
        if user.status_code == 401:
            return {'error': 'El token no es válido o está vencido.'}, 401
        else:
            user_base = json.loads(user.content.decode('utf-8'))
        post_ms_url = 'http://{}/posts/{}'.format(POST_MS, id)
        post = requests.get(post_ms_url, headers={'Authorization': auth_token})
        if post.status_code == 200:
            base_post = json.loads(post.content.decode('utf-8'))
            bp_userId = base_post['userId']
            if bp_userId != user_base['id']:
                return {'error': 'No se puede ver una publicación que no es propia.'}, 412
            bp_id = base_post['id']
            bp_createdAt = base_post['createdAt']
            bp_plannedStartDate = base_post['plannedStartDate']
            bp_plannedEndDate = base_post['plannedEndDate']
            route_ms_url = 'http://{}/routes/{}'.format(ROUTE_MS, base_post['routeId'])
            route = requests.get(route_ms_url, headers={'Authorization': auth_token})
            if route.status_code == 200:
                base_route = json.loads(route.content.decode('utf-8'))
                br_id = base_route['id']
                br_sourceAirportCode = base_route['sourceAirportCode']
                br_sourceCountry = base_route['sourceCountry']
                br_destinyAirportCode = base_route['destinyAirportCode']
                br_destinyCountry = base_route['destinyCountry']
                list_utilidades_publicacion = Utilidad.query.filter_by(idPost=id).all()
                Utilidades_Sorted = sorted(list_utilidades_publicacion, key=lambda x: utilidad_schema.dump(x)['utilidadOferta'], reverse=True)
                ofertas = []
                if Utilidades_Sorted is not None:
                    for utilidad in Utilidades_Sorted:
                        offer_ms_url = 'http://{}/offers/{}'.format(OFFER_MS, utilidad.idOferta)
                        offer = requests.get(offer_ms_url, headers={'Authorization': auth_token})
                        if offer.status_code == 200:
                            base_offer = json.loads(offer.content.decode('utf-8'))
                            bo_id = base_offer['id']
                            bo_userId = base_offer['userId']
                            bo_createdAt = base_offer['createdAt']
                            bo_description = base_offer['description']
                            bo_size = base_offer['size']
                            bo_fragile = base_offer['fragile']
                            bo_offer = base_offer['offer']
                            bo_score = utilidad.utilidadOferta
                            ofertas.append({
                                'id': bo_id,
                                'userId': bo_userId,
                                'description': bo_description,
                                'size': bo_size,
                                'fragile': bo_fragile,
                                'offer': bo_offer,
                                'score': bo_score,
                                'createdAt': bo_createdAt,
                            })
                        else:
                            return json.loads(offer.content.decode('utf-8')), 404
                
                return {
                    "data": {
                        "id": bp_id,
                        "route": {
                            "id": br_id,
                            "origin": {
                                "airportCode": br_sourceAirportCode,
                                "country": br_sourceCountry
                            },
                            "destiny": {
                                "airportCode": br_destinyAirportCode,
                                "country": br_destinyCountry
                            }
                        },
                        "plannedStartDate": bp_plannedStartDate,
                        "plannedEndDate": bp_plannedEndDate,
                        "createdAt": bp_createdAt,
                        "offers": ofertas
                    },
                }, 200
            else:
                return json.loads(route.content.decode('utf-8')), 404
        else:
            return json.loads(post.content.decode('utf-8')), 404