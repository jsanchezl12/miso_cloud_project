import sys
import os
os.environ['DATABASE_URL'] = 'sqlite:///sidecarapibd.db'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# test Api-management
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

def generate_random_credentials():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email = username + '@example.com'
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, email, password


class TestVistaSideCar(unittest.TestCase):
    random_username, random_email, random_password = generate_random_credentials()
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
        response = self.client.get('/ping')
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
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }

        mock_response_publishoffer = MagicMock()
        mock_response_publishoffer.status_code = 200
        mock_response_publishoffer.json.return_value = {
            "data": {
                "id": 3,
                "userId": 2,
                "createdAt": "2023-03-04 19:32:51.329715",
                "route": {
                    "id": 3,
                    "createdAt": "2023-03-04 19:32:51.288228",
                    "expireAt": "2023-04-03 19:32:51.285283"
                }
            },
            "msg": "Ruta y Publicación creada con éxito."
        }


        auth_token = create_access_token(identity='1234567890')
        with patch('requests.post',side_effect=[mock_response_publishoffer]) as post_mock:
        #patch('requests.post', return_value=mock_response):
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
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }

        mock_response_postoffer = MagicMock()
        mock_response_postoffer.status_code = 200
        mock_response_postoffer.json.return_value = {
            "data": {
                "id": 4,
                "userId": 1,
                "createdAt": "2023-03-04 19:41:27.833590",
                "postId": 2
            },
            "msg": "Oferta creada con éxito."
        }

        auth_token = create_access_token(identity='1234567890')
        #with patch('requests.get', return_value=mock_response):
        with patch('requests.post',side_effect=[mock_response_postoffer]) as post_mock:
            response = self.client.post('/public/posts/1/offers', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print(response_data)
            response_data = response_data['data']
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("postId", response_data)
            self.assertIn("createdAt", response_data)
    
    def test_search_post(self):
        mock_response = MagicMock()
        mock_response.status_code = 20
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }

        mock_response_searchpost = MagicMock()
        mock_response_searchpost.status_code = 200
        mock_response_searchpost.json.return_value = {
            "data": {
                "id": 1,
                "route": {
                    "id": 2,
                    "origin": {
                        "airportCode": "LAX",
                        "country": "COL"
                    },
                    "destiny": {
                        "airportCode": "BOG",
                        "country": "USA"
                    }
                },
                "plannedStartDate": "2023-03-20 00:00:00",
                "plannedEndDate": "2023-03-27 00:00:00",
                "createdAt": "2023-03-04 05:50:40.482852",
                "offers": [
                    {
                        "id": 2,
                        "userId": 1,
                        "description": "iPad",
                        "size": "MEDIUM",
                        "fragile": 'true',
                        "offer": 900,
                        "score": 800,
                        "createdAt": "2023-03-04 05:51:49.455174"
                    },
                    {
                        "id": 4,
                        "userId": 1,
                        "description": "iPad",
                        "size": "MEDIUM",
                        "fragile": 'true',
                        "offer": 900,
                        "score": 800,
                        "createdAt": "2023-03-04 19:41:27.833590"
                    }
                ]
            }
        }

        auth_token = create_access_token(identity='1234567890')
        #with patch('requests.get', return_value=mock_response):
        with patch('requests.get',side_effect=[mock_response_searchpost]) as get_mock:
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
        
    def test_create_user(self):     
        data_create = {
            "username": self.random_username,
            "email": self.random_email,
            "password": self.random_password
        }   

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "createdAt": "2023-03-04 19:41:27.833590"
        }
        with patch('requests.post', return_value=mock_response):
            response = self.client.post('/users/', data=json.dumps(data_create), content_type='application/json')
            response_data = json.loads(response.get_data(as_text=True))
            print(response_data)
            self.assertEqual(response.status_code, 201)
            self.assertIn("id", response_data)
            self.assertIn("createdAt", response_data)
    
    def test_get_info_usuario_validate_token(self):
        data_get_token = {
            "username": self.random_username,
            "password": self.random_password
        } 

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 2,
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3Nzk1OTE5MSwianRpIjoiNzFmNGQxN2MtZjBhMi00NTNlLThmODUtMGMwOGJmMjViNWIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1YW5zZSIsIm5iZiI6MTY3Nzk1OTE5MSwiZXhwIjoxNjc3OTYwOTkxfQ.p7KSNW9oWE2lOrR5bBk6ORI85XyDhJ3Yo7wswkxzmYE",
            "expireAt": "2023-03-04 20:16:31.325884"
        }
        
        mock_response_getuser = MagicMock()
        mock_response_getuser.status_code = 200
        mock_response_getuser.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        with patch('requests.post',side_effect=[mock_response]) as post_mock , \
            patch('requests.get', side_effect=[mock_response_getuser]) as get_mock: 
            #patch('requests.get', return_value=mock_response):
            response = self.client.post('/users/auth', data=json.dumps(data_get_token), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            self.assertIn("id", response_data)
            self.assertIn("token", response_data)
            self.assertIn("expireAt", response_data)
            self.token_ = response_data["token"]
            print("Test Users/me: -----------------")
            response = self.client.get('/users/me', headers={'Authorization': 'Bearer ' + self.token_})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            self.assertIn("id", response_data)
            self.assertIn("username", response_data)
            self.assertIn("email", response_data)
