"""
    This file contains all test needed to authentication users.
    It tests for both login and sign up functionality
"""

import unittest
from app import create_app
from flask import jsonify, json

app = create_app()


class FlaskUserTest(unittest.TestCase):
    """
        This class will cover all API endpoints for authentication
    """

    def setUp(self):
        """Initialize the reusable parts """
        user_signup_data = {"first_name": "Joseph",
                            "last_name": "Mutiga",
                            "other_names": "Kirega",
                            "phonenumber": "0716570355",
                            "email": "joseph.mutiga934@gmail.com",
                            "username": "joedfs",
                            "password": "1234"}
        duplicate_username_signup_data = {"first_name": "Joseph",
                                          "last_name": "Mutiga",
                                          "other_names": "Kirega",
                                          "phonenumber": "0716570355",
                                          "email": "joseph.mutiga@gmail.com",
                                          "username": "kirega",
                                          "password": "1234"}
        duplicate_email_signup_data = {"first_name": "Joseph",
                                       "last_name": "Mutiga",
                                       "other_names": "Kirega",
                                       "phonenumber": "0716570355",
                                       "email": "kirega@gmail.com",
                                       "username": "joe",
                                       "password": "1234"}
        wrong_signup_data = {"first_name": "Joseph",
                             "last_name": "Mutiga",
                             "other_names": "Kirega",
                             "email": "joseph.mutiga@gmail.com",
                             "username": "joe",
                             "password": "1234"}
        admin_signup_data = {"first_name": "Joseph",
                             "last_name": "Mutiga",
                             "other_names": "Kirega",
                             "phonenumber": "0716570355",
                             "email": "joseph.mutiga@gmail.com",
                             "username": "joep",
                             "password": "1234",
                             "isAdmin": True}
        login_data = {"username": "kirega", "password": "1234"}
        wrong_login_data = {"username": "joe", "password": "12345"}
        self.app = app.test_client()
        self.app.testing = True
        self.user_data = json.dumps(user_signup_data)
        self.admin_data = json.dumps(admin_signup_data)
        self.login_data = json.dumps(login_data)
        self.wrong_login_data = json.dumps(wrong_login_data)
        self.wrong_signup_data = json.dumps(wrong_signup_data)
        self.duplicate_username_signup_data = json.dumps(
            duplicate_username_signup_data)
        self.duplicate_email_signup_data = json.dumps(
            duplicate_email_signup_data
        )

    def test_user_can_signup(self):
        "Test that by posting user data to the endpoint, it gets created"
        result = self.app.post('/api/v1/signup', data=self.user_data)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Sign Up successful. Welcome!")

    def test_user_signup_with_wrong_data(self):
        "Test that by posting user data to the endpoint, it doest not get created"
        result = self.app.post('/api/v1/signup', data=self.wrong_signup_data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_admin_can_signup(self):
        "Test that by posting admin data to the endpoint, it gets created"
        result = self.app.post('/api/v1/signup', data=self.admin_data)
        print(result)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Sign Up successful. Welcome!")

    def test_login_with_right_credentials(self):
        """Test that a user/admin providing correct credentials in able to login"""
        result = self.app.post('/api/v1/login', data=self.login_data)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Login Success!")

    def test_login_with_wrong_credentials(self):
        """Test that a user providing correct credentials in able to login"""
        result = self.app.post('/api/v1/login', data=self.login_data)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Login Failed!")

    def test_sign_up_existing_username(self):
        """"Tests that a username and email are unique"""
        result = self.app.post(
            '/api/v1/signup', data=self.duplicate_username_signup_data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Username already exists")

    def test_sign_up_existing_email(self):
        """"Tests that a username and email are unique"""
        result = self.app.post(
            '/api/v1/signup', data=self.duplicate_email_signup_data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Email already exists")
