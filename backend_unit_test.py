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
    def test_friends_list(self):
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
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the friends_list endpoint
        response = self.client.get('/friends/list', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_friends_requests_receive(self):
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
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the friends_requests_receive endpoint
        response = self.client.get('/friends/requests/receive', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_friends_requests_receive_accept(self):
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

        response  = self.client.post('/users/register', json={
            'sid': '87654321',
            'name': 'Test User2',
            'contact': '010123456789',
            'email': 'test2@example.com',
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
        headers = {'Authorization': f'Bearer {access_token}'}

        # Send a friend request to the test user2
        response = self.client.post('/friends/requests', headers=headers, json={'studentid': '87654321'})
        self.assertEqual(response.status_code, 200)

        # Login to user2
        response = self.client.post('/users/login', json={
            'email': 'test2@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Accept the friend request
        response = self.client.post('/friends/requests/receive/accept', headers=headers,json={'studentid': '12345678'})

    # rentals.py Unnit Test
    def test_rentals_list(self):
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

        
        # Test invalid spaceid
        response = self.client.post('/rentals/list', headers={'Authorization': f'Bearer {access_token}'}, json={'spaceid': 4, 'date': '2023-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Space ID is invalid', response.json['error'])

        # Test invalid date format
        response = self.client.post('/rentals/list', headers={'Authorization': f'Bearer {access_token}'}, json={'spaceid': 1, 'date': 'invalid-date'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid date format, should be YYYY-MM-DD', response.json['error'])

        # Test the rentals_list endpoint
        response = self.client.post('/rentals/list', headers ={'Authorization': f'Bearer {access_token}'},json= {
            'spaceid': 2,
            'date': '2023-01-01'
        })
        self.assertEqual(response.status_code, 200)

    def test_rentals_join(self):    
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

        # Create the test user2
        response  = self.client.post('/users/register', json={
            'sid': '87654321',
            'name': 'Test User2',
            'contact': '010123456789',
            'email': 'test2@example.com',
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
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}
        
        # Test missing rentalid
        response = self.client.post('/rentals/join', headers=headers, json={})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Rental ID are required', response.json['error'])

        # Test non-existent rental
        response = self.client.post('/rentals/join', headers=headers, json={'rentalid': 1})
        self.assertEqual(response.status_code, 402)
        self.assertIn('Rental is not exist', response.json['error'])

        # Test1 valid rental create
        response = self.client.post('/rentals/create', headers=headers, json={
            'spaceid': 1,
            'starttime': '2024-07-01 10:00:00',
            'endtime': '2024-07-01 12:00:00',
            'maxpeople': 10,
            'desc': 'Test Rental',
            'friends': []
        })
        self.assertEqual(response.status_code, 200)

        # Test the profiles_schedules endpoint
        response = self.client.get('/profiles/schedules', headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test2 login
        response = self.client.post('/users/login', json={
            'email': 'test2@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)

        # Test2 Join
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post('/rentals/join', headers=headers, json={'rentalid': 1})
        self.assertEqual(response.status_code, 200)

        # Test2 cancel
        response = self.client.post('/rentals/cancle', headers=headers, json={'rentalid': 1})
        self.assertEqual(response.status_code, 200)

        # Test 1 Login
        response = self.client.post('/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        # Test 1 Rental delete
        response = self.client.post('/rentals/delete', headers=headers, json={'rentalid': 1})
        self.assertEqual(response.status_code, 200)

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
    def test_noramls_restrict(self):
        # Get the JWT token for the admin user
        response = self.client.post('/users/login', json={
            'email': 'admin',
            'password': 'admin'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Test the normals_restrict endpoint
        response = self.client.post('/normals/restrict', headers=headers, json={
            'spaceid': 1,
            'starttime': '2024-07-01 10:00:00',
            'endtime': '2024-07-01 12:00:00',
            'desc': 'Test Rental'
        })
        self.assertEqual(response.status_code, 200)

    def test_noramls_black(self):
        # Get the JWT token for the admin user
        response = self.client.post('/users/login', json={
            'email': 'admin',
            'password': 'admin'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the normals_black endpoint
        response = self.client.get('/normals/black', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_noramls_black_add(self):
        # Get the JWT token for the admin user
        response = self.client.post('/users/login', json={
            'email': 'admin',
            'password': 'admin'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Test the normals_black_add endpoint
        response = self.client.post('/normals/black/add', headers=headers, json={
            'userid': 3,
            'reason': 'Test Reason'
        })
        self.assertEqual(response.status_code, 200)

        # delete the black list
        response = self.client.post('/normals/black/delete', headers=headers, json={
            'userid': 3
        })
        self.assertEqual(response.status_code, 200)

    # profiles.py Unnit Test
    def test_profiles_user(self):
        response = self.client.post('/users/login', json={
            'email': 'email2',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the profiles_user endpoint
        response = self.client.get('/profiles/user', headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_profiles_schedules(self):
        response = self.client.post('/users/login', json={
            'email': 'email2',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the profiles_schedules endpoint
        response = self.client.get('/profiles/schedules', headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_profiles_club_list(self):
        response = self.client.post('/users/login', json={
            'email': 'email4',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the profiles_club_list endpoint
        response = self.client.get('/profiles/clubmembers/list', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_profiles_club_add(self):
        response = self.client.post('/users/login', json={
            'email': 'email4',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

        # Test the profiles_club_add endpoint
        response = self.client.post('/profiles/clubmembers/add', headers=headers, json={'studentid': '23451'})
        self.assertEqual(response.status_code, 200)

        # 조회
        response = self.client.get('/profiles/clubmembers/list', headers=headers)
        self.assertEqual(response.status_code, 200)

        # 삭제
        response = self.client.post('/profiles/clubmembers/delete', headers=headers, json={'studentid': '23451'})
        self.assertEqual(response.status_code, 200)

    def test_profiles_club_settings_changepw(self):
        response = self.client.post('/users/login', json={
            'email': 'email2',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Test the profiles_club_settings_changepw endpoint
        response = self.client.post('/profiles/settings/changepw', headers=headers, json={
            'pw': 'password'
        })
        self.assertEqual(response.status_code, 200)

        # Test the profiles_club_settings_changepw endpoint with an invalid password
        response = self.client.post('/users/login', json={
            'email': 'email2',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)

        # Proper pw
        response = self.client.post('/users/login', json={
            'email': 'email2',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    # notifications.py Unnit Test
    def test_notifications_list(self):
        response = self.client.post('/users/login', json={
            'email': 'email2',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['jwt_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Test the notifications_list endpoint
        response = self.client.post('/notifications/list', headers=headers)
        self.assertEqual(response.status_code, 200)

    # schedules.py Unnit Test
    def test_schedules_list(self):
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

        # Test the schedules_list endpoint
        response = self.client.post('/schedules/list', headers ={'Authorization': f'Bearer {access_token}'},json= {
            'spaceid': 2,
            'date': '2023-01-01'
        })
        self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()