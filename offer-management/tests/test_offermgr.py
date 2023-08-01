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
    rand_descriptiony = fake_str(50)
    rand_filter  = "me"
    rand_post = "1"
    bagCost = 100

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.token_ = ''
    
    def test_health_check(self):
        response = self.client.get('/offers/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"pong"\n')
    
    def test_create_offer(self):
        data_create = {
            "postId": 1,
            "description": self.rand_descriptiony,
            "size": "SMALL",
            "fragile": True,
            "offer": 100
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
            response = self.client.post('/offers/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.get_data(as_text=True))
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("createdAt", response_data)

    def test_delete_offer(self):
        data_create = {
            "postId": 1,
            "description": self.rand_descriptiony,
            "size": "SMALL",
            "fragile": True,
            "offer": 100
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
            response = self.client.post('/offers/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            Url_id_eliminate = '/offers/'+ str(response_data['id'])
            response = self.client.delete(Url_id_eliminate, data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)

    def test_update_offer(self):
        data_create = {
            "postId": 1,
            "description": self.rand_descriptiony,
            "size": "SMALL",
            "fragile": True,
            "offer": 100
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
            response = self.client.post('/offers/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))

            data_update = {
                "postId": 2,
                "description": self.rand_descriptiony,
                "size": "LARGE",
                "fragile": True,
                "offer": 1000
            } 
            Url_id_eliminate = '/offers/'+ str(response_data['id'])
            response = self.client.put(Url_id_eliminate, data=json.dumps(data_update), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("createdAt", response_data)
            self.assertEqual(str(response_data["size"]), "LARGE")
        
    def test_get_offer(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            response = self.client.get('/offers/1', headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            self.assertIn("id", response_data)
            self.assertIn("postId", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("description", response_data)
            self.assertIn("size", response_data)
            self.assertIn("fragile", response_data)
            self.assertIn("offer", response_data)
            self.assertIn("createdAt", response_data)
    
    def test_get_search_offer(self):
        mock_response = MagicMock()
        mock_response.status_code = 20
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            url = f'/offers?post={self.rand_post}&filter={self.rand_filter}'
            print(url)
            response = self.client.get(url, headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            routes = response_data
            for route in routes:
                self.assertIn("id", route)
                self.assertIn("postId", route)
                self.assertIn("userId", route)
                self.assertIn("description", route)
                self.assertIn("size", route)
                self.assertIn("offer", route)
                self.assertIn("createdAt", route)