import sys
import os
os.environ['DATABASE_URL'] = 'sqlite:///utilitym.db'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# test utility-management
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from app import app
import json
import random
import string
from flask_restful import Api
from flask import Flask
from flask_restful import Resource
from flask_jwt_extended import create_access_token

def fake_str(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str.upper()


class TestUtilityMgr(unittest.TestCase):
    rand_sourceAirportCode = fake_str(3)
    rand_descriptiony = fake_str(50)
    rand_filter  = "me"
    rand_when = "2023-03-02"
    rand_route = "1"
    bagCost = 100

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.token_ = ''
    
    def test_health_check(self):
        response = self.client.get('/public/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"pong"\n')
    
    def test_public_Post(self):
        data_create = {
            "plannedStartDate": "03/15/2023",
            "plannedEndDate": "03/20/2023",
            "origin":{ 
                "airportCode": "10",
                "country": "Colombia"},
            "destiny":{ 
                "airportCode": "5",
                "country": "Peru"},
            "bagCost": 5000
        }  
        print('Data--->',data_create)
        mock_response_getuser = MagicMock()
        mock_response_getuser.status_code = 200
        mock_response_getuser.content.decode.return_value = json.dumps({ "id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com" })

        mock_response_getroute = MagicMock()
        mock_response_getroute.status_code = 200
        mock_response_getroute.content.decode.return_value = json.dumps({'error': 'no se encontraron trayectos con esas caracteristicas'})
        mock_response_getroute.content.__contains__.return_value = True

        mock_response_postcroute = MagicMock()
        mock_response_postcroute.status_code = 201
        mock_response_postcroute.content.decode.return_value = json.dumps({'id': 1, 'createdAt': '03/20/2023', 'expireAt': '04/20/2023'})
    
        mock_responde_postcpost = MagicMock()
        mock_responde_postcpost.status_code = 201
        mock_responde_postcpost.content.decode.return_value = json.dumps({'id': 1, 'userId': 1, 'createdAt': '03/20/2023'})

        mock_response_getroute = MagicMock()
        mock_response_getroute.status_code = 200
        mock_response_getroute.content.decode.return_value = json.dumps({'error': 'no se encontraron trayectos con esas caracteristicas'})
        mock_response_getroute.content.__contains__.return_value = True

        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', side_effect=[mock_response_getuser,mock_response_getroute]) as get_mock, \
            patch('requests.post',side_effect=[mock_response_postcroute,mock_responde_postcpost]) as post_mock:
            response = self.client.post('/public/posts', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print('Response--->',response_data)
            response_data = response_data['data']
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("createdAt", response_data)
            self.assertIn("route",response_data)
    
    def test_public_Post2(self):
        data_create = {
            "plannedStartDate": "03/15/2023",
            "plannedEndDate": "03/20/2023",
            "origin":{ 
                "airportCode": "10",
                "country": "Colombia"},
            "destiny":{ 
                "airportCode": "5",
                "country": "Peru"},
            "bagCost": 5000
        }  
        print('Data--->',data_create)
        mock_response_getuser = MagicMock()
        mock_response_getuser.status_code = 200
        mock_response_getuser.content.decode.return_value = json.dumps({ "id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com" })

        mock_response_getroute = MagicMock()
        mock_response_getroute.status_code = 200
        mock_response_getroute.content.decode.return_value = json.dumps([
            {
                "id": 2,
                "sourceAirportCode": "LAX",
                "sourceCountry": "COL",
                "destinyAirportCode": "BOG",
                "destinyCountry": "USA",
                "bagCost": 200,
                "createdAt": "2023-03-04 05:50:40.441845",
                "expireAt": "2023-04-03 05:50:40.441845"
            }
        ])

        mock_response_getpost= MagicMock()
        mock_response_getpost.status_code = 200
        mock_response_getpost.content.decode.return_value = json.dumps({'error': 'no se encontraron publicaciones con esas caracteristicas'})
        mock_response_getpost.content.__contains__.return_value = True
        
        mock_responde_postcpost = MagicMock()
        mock_responde_postcpost.status_code = 201
        mock_responde_postcpost.content.decode.return_value = json.dumps({'id': 1, 'userId': 1, 'createdAt': '03/20/2023'})

        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', side_effect=[mock_response_getuser,mock_response_getroute, mock_response_getpost]) as get_mock, \
            patch('requests.post',side_effect=[mock_responde_postcpost]) as post_mock:
            response = self.client.post('/public/posts', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print('Response--->',response_data)
            response_data = response_data['data']
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("createdAt", response_data)
            self.assertIn("route",response_data)
    
    def test_public_Post3(self):
        data_create = {
            "plannedStartDate": "03/15/2023",
            "plannedEndDate": "03/20/2023",
            "origin":{ 
                "airportCode": "10",
                "country": "Colombia"},
            "destiny":{ 
                "airportCode": "5",
                "country": "Peru"},
            "bagCost": 5000
        }  
        print('Data--->',data_create)
        mock_response_getuser = MagicMock()
        mock_response_getuser.status_code = 200
        mock_response_getuser.content.decode.return_value = json.dumps({ "id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com" })

        mock_response_getroute = MagicMock()
        mock_response_getroute.status_code = 200
        mock_response_getroute.content.decode.return_value = (
        json.dumps([
            {
                "id": 2,
                "sourceAirportCode": "LAX",
                "sourceCountry": "COL",
                "destinyAirportCode": "BOG",
                "destinyCountry": "USA",
                "bagCost": 200,
                "createdAt": "2023-03-04 05:50:40.441845",
                "expireAt": "2023-04-03 05:50:40.441845"
            }]
        ))

        mock_response_getpost= MagicMock()
        mock_response_getpost.status_code = 200
        mock_response_getpost.content.decode.return_value = json.dumps([
            {
                "id": 2,
                "routeId": 2,
                "userId": 2,
                "plannedStartDate": "2023-03-20 00:00:00",
                "plannedEndDate": "2023-03-27 00:00:00",
                "createdAt": "2023-03-04 05:50:40.482852"
            }
        ])
        
        mock__response_updatepost = MagicMock()
        mock__response_updatepost.status_code = 200
        mock__response_updatepost.content.decode.return_value = json.dumps({
            "id": 2,
            "routeId": "1",
            "userId": 2,
            "plannedStartDate": "2023-02-13 00:00:00",
            "plannedEndDate": "2023-02-27 00:00:00",
            "createdAt": "2023-03-04 05:50:40.482852"
        })

        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', side_effect=[mock_response_getuser,mock_response_getroute, mock_response_getpost]) as get_mock, \
            patch('requests.put',side_effect=[mock__response_updatepost]) as put_mock :
            response = self.client.post('/public/posts', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print('Response--->',response_data)
            response_data = response_data['data']
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("createdAt", response_data)
            self.assertIn("route",response_data)

    def test_public_offert(self):
        data_create = {
            "description": "descripción del paquete a llevar",
            "size": "LARGE",
            "fragile": "true",
            "offer": "5000"
        }  
        print('Data--->',data_create)
        mock_response_getuser = MagicMock()
        mock_response_getuser.status_code = 200
        mock_response_getuser.json.return_value = json.dumps({ "id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com"})
        mock_response_getuser.content.decode.return_value = json.dumps({ "id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com"})

        mock_response_getpost = MagicMock()
        mock_response_getpost.status_code = 200
        mock_response_getpost.content.decode.return_value = json.dumps({
            "id": 1,
            "routeId": "1",
            "userId": 2,
            "plannedStartDate": "2023-03-20 00:00:00",
            "plannedEndDate": "2023-03-27 00:00:00",
            "createdAt": "2023-03-10 05:50:40.482852"
        })

        mock_response_getroute = MagicMock()
        mock_response_getroute.status_code = 200
        mock_response_getroute.content.decode.return_value = json.dumps({
            "id": 1,
            "sourceAirportCode": "LAX",
            "sourceCountry": "COL",
            "destinyAirportCode": "BOG",
            "destinyCountry": "USA",
            "bagCost": 200,
            "createdAt": "2023-03-04 05:50:40.441845",
            "expireAt": "2023-04-03 05:50:40.441845"
        })

        mock_response_postoffer = MagicMock()
        mock_response_postoffer.status_code = 201
        mock_response_postoffer.content.decode.return_value = json.dumps({
            "id": 3,
            "userId": 2,
            "createdAt": "2023-03-04 17:27:08.041247"
        })

        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', side_effect=[mock_response_getuser,mock_response_getpost,mock_response_getroute]) as get_mock, \
            patch('requests.post',side_effect=[mock_response_postoffer]) as post_mock:
            response = self.client.post('/public/posts/1/offers', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print('Response--->',response_data)
            response_data = response_data['data']
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("postId", response_data)
            self.assertIn("createdAt", response_data)
    
    def test_search_post(self):
        mock_response_getuser = MagicMock()
        mock_response_getuser.status_code = 20
        mock_response_getuser.json.return_value = {"id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com"}
        mock_response_getuser.content.decode.return_value = json.dumps({ "id": 1, "username": "ravelinx", "email": "drummerwilliam@gmail.com"})

        mock_response_getpost = MagicMock()
        mock_response_getpost.status_code = 200
        mock_response_getpost.content.decode.return_value = json.dumps({
            "id": 1,
            "routeId": "1",
            "userId": 1,
            "plannedStartDate": "2023-03-20 00:00:00",
            "plannedEndDate": "2023-03-27 00:00:00",
            "createdAt": "2023-03-10 05:50:40.482852"
        })

        mock_response_getroute = MagicMock()
        mock_response_getroute.status_code = 200
        mock_response_getroute.content.decode.return_value = json.dumps({
            "id": 1,
            "sourceAirportCode": "LAX",
            "sourceCountry": "COL",
            "destinyAirportCode": "BOG",
            "destinyCountry": "USA",
            "bagCost": 200,
            "createdAt": "2023-03-04 05:50:40.441845",
            "expireAt": "2023-04-03 05:50:40.441845"
        })

        mock_response_getoffer = MagicMock()
        mock_response_getoffer.status_code = 200
        mock_response_getoffer.content.decode.return_value = json.dumps({
            "id": 2,
            "postId": "2",
            "userId": 1,
            "description": "iPad",
            "size": "MEDIUM",
            "fragile": 'true',
            "offer": 900,
            "createdAt": "2023-03-04 05:51:49.455174"
        })
        auth_token = create_access_token(identity='1234567890')
        #with patch('requests.get', return_value=mock_response):
        with patch('requests.get', side_effect=[mock_response_getuser,mock_response_getpost,mock_response_getroute,mock_response_getoffer]) as get_mock:
            response = self.client.get('/public/posts/1', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print('Response--->',response_data)
            response_data = response_data['data']
            self.assertEqual(response.status_code, 200)
            self.assertIn("id",response_data)
            self.assertIn("route",response_data)
            self.assertIn("plannedStartDate",response_data)
            self.assertIn("plannedEndDate",response_data)
            self.assertIn("createdAt",response_data)
            self.assertIn("offers",response_data)
            offers = response_data['offers']
            for offer in offers:
                self.assertIn("id", offer)
                self.assertIn("userId", offer)
                self.assertIn("description", offer)
                self.assertIn("size", offer)
                self.assertIn("fragile", offer)
                self.assertIn("offer", offer)
                self.assertIn("score", offer)
                self.assertIn("createdAt", offer)