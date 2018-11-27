"""
this file will include all the view endpoints for the application.
"""

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import User

# default User
default_user = User(
    userid=1,
    first_name="Joseph",
    last_name="Mutiga",
    other_names="Kirega",
    phonenumber="0716570355",
    email="kirega@gmail.com",
    username="kirega",
    password="1234",
    isAdmin=True
)
user_db = [default_user]


class SignUp(Resource):
    def __init__(self):
        self.users = user_db

    def post(self):
        data = request.get_json(force=True)
        print(data)
        list_of_fields = ['first_name', "last_name", "other_names", "phonenumber", "email",
                          "email", "username", "password"]
        if not data:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)

        # checks that all the fields are there
        if all(i in data for i in list_of_fields):
            # Ensure unique usernames and emails
            for user in self.users:
                print(user)
                if user.username == data['username']:
                    return make_response(jsonify({"message": "Username already exists"}), 400)
                if user.email == data['email']:
                    return make_response(jsonify({"message": "Email already exists"}), 400)

            # Auto increment ids for all new users.
            userid = len(self.users) + 1
            if 'isAdmin' in data:
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
