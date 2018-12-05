"""
    This file contains all test needed to authentication users.
    It tests for both login and sign up functionality
"""

from ... import create_app
from flask import json
from .basetest import BaseTestCase


class FlaskUserTest(BaseTestCase):
    """
        This class will cover all API endpoints for authentication
    """

    def test_user_signup_with_empty_body(self):
        result = self.app.post('/api/v1/signup', data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_user_login_with_empty_body(self):
        result = self.app.post('/api/v1/login', data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

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
        result = self.app.post('/api/v1/login', data=self.wrong_login_data)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Login Failed!")

    def test_login_with_wrong_format(self):
        """Test that a user providing correct credentials in able to login"""
        result = self.app.post(
            '/api/v1/login', data=self.wrong_login_data_format)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_login_with_nonexisting_user(self):
        """Test that a user providing correct credentials in is unable to login
         if user does not exist"""
        result = self.app.post(
            '/api/v1/login', data=self.nonexisting_user)
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


