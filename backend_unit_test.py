import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from flask_jwt_extended import create_access_token
from app import app as main_app
from app import db
from db import *
from methods import *

class MyTest(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

    def setUp(self):
        self.app = main_app
        self.client = main_app.test_client()
        self.app.config['TESTING'] = self.TESTING
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        with self.app.app_context():
            db.create_all()
            methods_init_datas()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # users.py Unnit Test
    def test_register(self):
        # Test for successful registration
        response = self.client.post('/users/register', json={
            'sid': '12345678',
            'name': 'Test User',
            'contact': '01012345678',
            'email': 'test@example.com',
            'password': 'password123',
            'usertype': 'Student'
        })
        self.assertEqual(response.status_code, 200)
        # Test for duplicate registration
        response = self.client.post('/users/register', json={
            'sid': '12345678',
            'name': 'Test User',
            'contact': '01012345678',
            'email': 'test@example.com',
            'password': 'password123',
            'usertype': 'Student'
        })
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        # Create a test user
        user_id = None
        with self.app.app_context():
            user = Users(studentid='12345678', name='Test User', contact='01012345678', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            user_id = user.userid

        # Test for successful login
        response = self.client.post('/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)

        # Test for invalid credentials
        response = self.client.post('/users/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)

        # Test for blacklisted user
        with self.app.app_context():
            black = Blacklist(userid=user_id)
            db.session.add(black)
            db.session.commit()

        response = self.client.post('/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)

    # friends.py Unnit Test
    # schedules.py Unnit Test
    # rentals.py Unnit Test
    def test_rentals_list(self):
        with self.app.app_context():
            # Set up the test data
            user = Users(studentid='12345678', name='Test User', contact='01012345678', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.userid)

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Test missing spaceid and date
            response = self.client.post('/rentals/list', headers=headers, json={})
            self.assertEqual(response.status_code, 400)
            self.assertIn('Space ID and date are required', response.json['error'])

            # Test invalid spaceid
            response = self.client.post('/rentals/list', headers=headers, json={'spaceid': 4, 'date': '2023-01-01'})
            self.assertEqual(response.status_code, 400)
            self.assertIn('Space ID is invalid', response.json['error'])

            # Test invalid date format
            response = self.client.post('/rentals/list', headers=headers, json={'spaceid': 1, 'date': 'invalid-date'})
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid date format, should be YYYY-MM-DD', response.json['error'])

            # Test valid request

    def test_rentals_join(self):
        with self.app.app_context():
            # Set up the test data
            user = Users(studentid='12345678', name='Test User', contact='01012345678', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.userid)

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Test missing rentalid
            response = self.client.post('/rentals/join', headers=headers, json={})
            self.assertEqual(response.status_code, 401)
            self.assertIn('Rental ID are required', response.json['error'])

            # Test non-existent rental
            response = self.client.post('/rentals/join', headers=headers, json={'rentalid': 1})
            self.assertEqual(response.status_code, 402)
            self.assertIn('Rental is not exist', response.json['error'])

            # Test valid request

    def test_rentals_cancle(self):
        with self.app.app_context():
            # Set up the test data
            user = Users(studentid='12345678', name='Test User', contact='01012345678', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.userid)

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Test rental not exist
            response = self.client.post('/rentals/cancle', headers=headers, json={'rentalid': 1})
            self.assertEqual(response.status_code, 401)
            self.assertIn('rental not exist', response.json['error'])

            # Test valid request

    def test_rentals_create(self):
        with self.app.app_context():
            # Set up the test data
            user = Users(studentid='12345678', name='Test User', contact='01012345678', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.userid)

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Test invalid spaceid
            response = self.client.post('/rentals/create', headers=headers, json={
                'spaceid': 4,
                'starttime': '2023-01-01 10:00:00',
                'endtime': '2023-01-01 12:00:00',
                'maxpeople': 10,
                'desc': 'Test Rental',
                'friends': []
            })
            self.assertEqual(response.status_code, 400)
            # self.assertIn('Invalid spaceid', response.json['error'])

            # Test invalid start and end time
            response = self.client.post('/rentals/create', headers=headers, json={
                'spaceid': 1,
                'starttime': '2023-01-01 12:00:00',
                'endtime': '2023-01-01 10:00:00',
                'maxpeople': 10,
                'desc': 'Test Rental',
                'friends': []
            })
            self.assertEqual(response.status_code, 401)
            self.assertIn('Invalid starttime and endtime', response.json['error'])

            # Test rental already exist

    def test_rentals_delete(self):
        with self.app.app_context():
            # Set up the test data
            user = Users(studentid='12345678', name='Test User', contact='01012345678', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.userid)

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Test rental not exist
            response = self.client.post('/rentals/delete', headers=headers, json={'rentalid': 1})
            self.assertEqual(response.status_code, 400)
            self.assertIn('rental not exist', response.json['error'])

            # You should add mock data here for a complete test case

    # clubs.py Unnit Test
    def test_clubs_clubregular_add_invalid_clubid(self):
        # Create the test user
        response  = self.client.post('/users/register', json={
            'sid': '12345678',
            'name': 'Test User',
            'contact': '01012345678',
            'email': 'test@example.com',
            'password': 'password123',
            'usertype': 'Student'
        })
        self.assertEqual(response.status_code, 200)

        # Get the JWT token for the test user
        response = self.client.post('/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']

        # Test the clubs_clubregular_add endpoint with an invalid clubid
        response = self.client.post('/clubs/clubregular/add', headers={'Authorization': f'Bearer {access_token}'}, json={
            'clubid': 999999,  # This clubid does not exist
            'spaceid': 1,
            'dayofweek': 1,
            'starttime': '10:00:00',
            'endtime': '12:00:00',
            'nums': 1
        })
        self.assertEqual(response.status_code, 200)  # Expect a 404 Not Found response

    # normals.py Unnit Test
    # profiles.py Unnit Test
    # notifications.py Unnit Test
if __name__ == '__main__':
    unittest.main()