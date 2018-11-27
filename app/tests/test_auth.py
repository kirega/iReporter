"""
    This file contains all test needed to authentication users.
    It tests for both login and sign up functionality
"""

import unittest
from app import create_app
from flask import json

app = create_app()


class FlaskUserTest(unittest.TestCase):
    """
        This class will cover all API endpoints for authentication
    """

    def setUp(self):
        """Initialize the reusable parts """
        user_signup_data = {'first_name': 'Joseph', 'last_name': 'Mutiga', "other_names": "Kirega", "phonenumber": "0716570355",
                            'email': 'joseph.mutiga@gmail.com', 'username': 'joe', "password": "1234"}
        wrong_signup_data = {'first_name': 'Joseph', 'last_name': 'Mutiga', "other_names": "Kirega",
                             'email': 'joseph.mutiga@gmail.com', 'username': 'joe', "password": "1234"}
        admin_signup_data = {'first_name': 'Joseph', 'last_name': 'Mutiga', "other_names": "Kirega", "phonenumber": "0716570355",
                             'email': 'joseph.mutiga@gmail.com', 'username': 'joe', "password": "1234", "isAdmin": True}
        login_data = {"username": "joe", "password": "1234"}
        wrong_login_data = {"username": "joe", "password": "12345"}
        self.app = app.test_client()
        self.app.testing = True
        self.user_data = json.dumps(user_signup_data)
        self.admin_data = json.dumps(admin_signup_data)
        self.login_data = json.dumps(login_data)
        self.wrong_login_data = json.dumps(wrong_login_data)
        self.wrong_signup_data = json.dumps(wrong_signup_data)

    def test_user_can_signup(self):
        "Test that by posting user data to the endpoint, it gets created"
        result = self.app.post('/api/v1/users', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(json.loads([result.data]),
                         "Sign Up successful. Welcome!")

    def test_user_signup_with_wrong_data(self):
        "Test that by posting user data to the endpoint, it doest not get created"
        result = self.app.post('/api/v1/users', data=self.wrong_signup_data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(json.loads([result.data]),
                         "Missing or invalid field members")

    def test_admin_can_signup(self):
        "Test that by posting admin data to the endpoint, it gets created"
        result = self.app.post('/api/v1/users', data=self.admin_data)
        self.assertEqual(result.status_code, 201)

    def test_login_with_right_credentials(self):
        """Test that a user/admin providing correct credentials in able to login"""
        result = self.app.post('/api/v1/users', data=self.login_data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads([result.data]),
                         "Login Success!")

    def test_login_with_wrong_credentials(self):
        """Test that a user providing correct credentials in able to login"""
        result = self.app.post('/api/v1/users', data=self.login_data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(json.loads([result.data]),
                         "Login Failed!")
