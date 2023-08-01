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
from datetime import datetime, timedelta
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
    rand_when = "2023-03-02"
    rand_route = "1"
    bagCost = 100

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.token_ = ''
    
    def test_health_check(self):
        response = self.client.get('/posts/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'"pong"\n')
    
    def test_create_post(self):
        data_create = {
            "routeId": 1,
            "plannedStartDate": "2023-03-02",
            "plannedEndDate": "2023-03-05" 
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
            response = self.client.post('/posts/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            print('Response--->',response)
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.get_data(as_text=True))
            print(response_data)
            self.assertIn("id", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("createdAt", response_data)

    def test_delete_post(self):
        data_create = {
            "routeId": "1",
            "plannedStartDate": "2023-03-02",
            "plannedEndDate": "2023-03-04"
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
            response = self.client.post('/posts/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            Url_id_eliminate = '/posts/' + str(response_data['id'])
            response = self.client.delete(Url_id_eliminate, data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        data_create = {
            "routeId": "1",
            "plannedStartDate": "2023-03-02",
            "plannedEndDate": "2023-03-04"
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
            response = self.client.post('/posts/', data=json.dumps(data_create), content_type='application/json', headers={'Authorization': auth_token})
            response_data = json.loads(response.get_data(as_text=True))
            print(response_data)
            Url_id_eliminate = '/posts/' + str(response_data['id'])
            now = datetime.now()
            future = now + timedelta(days=3)
            data_update = {
                "routeId": 2,
                "plannedStartDate": '2023-03-02 00:00:00',
                "plannedEndDate": '2023-03-03 00:00:00'
            } 
        with patch('requests.get', return_value=mock_response):
            response = self.client.put(Url_id_eliminate, data=json.dumps(data_update), content_type='application/json', headers={'Authorization': auth_token})
            # response_data = json.loads(response.get_data(as_text=True))
            print(response)

            self.assertEqual(response.status_code, 200)
            # self.assertIn("id", response_data)
            # self.assertIn("userId", response_data)
            # self.assertIn("createdAt", response_data)
            # self.assertEqual(str(response_data["routeId"]), 2)
      
    def test_get_post(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            response = self.client.get('/posts/1', headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            print(response_data)
            self.assertIn("id", response_data)
            self.assertIn("routeId", response_data)
            self.assertIn("userId", response_data)
            self.assertIn("plannedStartDate", response_data)
            self.assertIn("plannedEndDate", response_data)
            self.assertIn("createdAt", response_data)
    
    def test_get_search_post(self):
        mock_response = MagicMock()
        mock_response.status_code = 20
        mock_response.json.return_value = {
            "id": 1,
            "username": "ravelinx",
            "email": "drummerwilliam@gmail.com"
        }
        auth_token = create_access_token(identity='1234567890')
        with patch('requests.get', return_value=mock_response):
            url = f'/posts?when={self.rand_when}&route={self.rand_route}&filter={self.rand_filter}'
            print(url)
            response = self.client.get(url, headers={'Authorization': auth_token})
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.get_data(as_text=True))
            routes = response_data
            for route in routes:
                self.assertIn("id", route)
                self.assertIn("routeId", route)
                self.assertIn("userId", route)
                self.assertIn("plannedStartDate", route)
                self.assertIn("plannedEndDate", route)
                self.assertIn("createdAt", route)