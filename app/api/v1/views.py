"""
this file will include all the view endpoints for the application.
"""

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import User

user_db = []


class SignUp(Resource):
    def __init__(self):
        self.users = user_db

    def post(self):
        data = request.get_json(force=True)
        list_of_fields = ['first_name', "last_name", "other_names", "phonenumber", "email",
                          "email", "username", "password"]
        if not data:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)

        if all(i in data for i in list_of_fields):
            userid = len(self.users) + 1 #Auto increment ids for all new users.
            if 'is_admin' in data:
                new_user = User(
                    userid=userid,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    other_names=data['other_names'],
                    phonenumber=data['phonenumber'],
                    email=data['email'],
                    username=data['username'],
                    password=data["password"],
                    isAdmin=data['isAdmin']
                )
            else:
                new_user = User(
                    userid=userid,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    other_names=data['other_names'],
                    phonenumber=data['phonenumber'],
                    email=data['email'],
                    username=data['username'],
                    password=data["password"]
                )
            self.users.append(new_user)
        else:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)

        return make_response(jsonify({"message": "Sign Up successful. Welcome!"}), 201)


class Login(Resource):
    pass
