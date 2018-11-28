"""
this file will include all the view endpoints for the application.
"""

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import User, Incident

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
    """"This endpoints handles all login posts"""

    def __init__(self):
        self.users = user_db

    def post(self):
        # check that the user exists and the password is correct.
        data = request.get_json(force=True)

        if not data:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)

        required_fields = ['username', 'password']
        if all(i in data for i in required_fields):
            for user in self.users:
                if user.username == data['username']:
                    if user.password == data['password']:
                        return make_response(jsonify({"message": "Login Success!"}), 200)
                    else:
                        return make_response(jsonify({"message": "Login Failed!"}), 401)

            return make_response(jsonify({"message": "User does not exist"}), 401)
        else:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)


class AllIncidents(Resource, Incident):
    """
        This endpoint handles the GET to get all incidents
        As well as POST for any new incident
    """

    def __init__(self):
        self.db = Incident()
        # default_user
        self.db.save("intervention",
                     "Police taking bribes",
                     "-1.28333, 36.81667",
                     "1",
                     ["https://wallpaperbrowse.com/media/images/soap-bubble-1958650_960_720.jpg",
                      "https://wallpaperbrowse.com/media/images/th.jpg"],
                     ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                      "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
                     )

    def get(self):
        return make_response(jsonify(self.db.db), 200)

    def post(self):
        data = request.get_json(force=True)
        required_fields = ["incidentType", "comment",
                           "location", "createdBy", "images", "videos"]

        if all(i in data for i in required_fields):
            self.db.save(data['incidentType'], data["comment"], data['location'],
                         data['createdBy'], data['images'], data['videos'])
            return make_response(jsonify({"message": "New incident created"}), 201)
        else:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)
