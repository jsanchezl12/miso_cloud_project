import sys
import os
os.environ['DATABASE_URL'] = 'sqlite:///routem.db'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# test route-management
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
# def generate_random_credentials():
#     username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#     email = username + '@example.com'
#     password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#     return username, email, password

def fake_str(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str.upper()


class TestVistaHealthCheck(unittest.TestCase):
    rand_sourceAirportCode = fake_str(3)
    rand_sourceCountry = fake_str(2)
    rand_destinationAirportCode = fake_str(3)
    rand_destinationCountry = fake_str(2)
    bagCost = 100

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.token_ = ''
    
    def test_health_check(self):
        response = self.client.get('/routes/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"pong"\n')
    
    def test_create_route(self):
        data_create = {
            "sourceAirportCode": self.rand_sourceAirportCode,
            "sourceCountry": self.rand_sourceCountry,
            "destinyAirportCode": self.rand_destinationAirportCode,
            "destinyCountry": self.rand_destinationCountry,
            "bagCost": 100
        }  
        print('Data--->',data_create)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            response = self.client.post('/routes/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            print('Response--->',response)
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.get_data(as_text=True))
            print(response_data)
            self.assertIn("id", response_data)
            self.assertIn("createdAt", response_data)
            self.assertIn("expireAt", response_data)
    
    def test_get_route(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            response = self.client.get('/routes/1', headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            self.assertIn("id", response_data)
            self.assertIn("sourceAirportCode", response_data)
            self.assertIn("sourceCountry", response_data)
            self.assertIn("destinyAirportCode", response_data)
            self.assertIn("destinyCountry", response_data)
            self.assertIn("bagCost", response_data)
    
    def test_get_search_route(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            url = f'/routes?from={self.rand_sourceAirportCode}&to={self.rand_destinationAirportCode}&when=2023-02-02'
            response = self.client.get(url, headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            routes = response_data
            for route in routes:
                self.assertIn("id", route)
                self.assertIn("sourceAirportCode", route)
                self.assertIn("sourceCountry", route)
                self.assertIn("destinyAirportCode", route)
                self.assertIn("destinyCountry", route)
                self.assertIn("bagCost", route)

    def test_delete_route(self):
        data_create = {
            "sourceAirportCode": "5",
            "sourceCountry": "Medellin",
            "destinyAirportCode": "3",
            "destinyCountry": "Cancun",
            "bagCost": "7000"
        }  
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            response = self.client.post('/routes/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            Url_id_eliminate = '/routes/' + str(response_data['id'])
            response = self.client.delete(Url_id_eliminate, data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)

    def test_update_route(self):
        data_create = {
            "sourceAirportCode": "5",
            "sourceCountry": "Medellin",
            "destinyAirportCode": "3",
            "destinyCountry": "Cancun",
            "bagCost": "7000"
        }  
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            response = self.client.post('/routes/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            Url_id_eliminate = '/routes/' + str(response_data['id'])

            data_uopdate = {
            "sourceAirportCode": "15",
            "sourceCountry": "Cartagena",
            "destinyAirportCode": "3",
            "destinyCountry": "Cancun",
            "bagCost": "7000"
        } 
            response = self.client.put(Url_id_eliminate, data=json.dumps(data_uopdate), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("sourceAirportCode", response_data)
            self.assertIn("createdAt", response_data)
            self.assertEqual(str(response_data["sourceCountry"]),"Cartagena")