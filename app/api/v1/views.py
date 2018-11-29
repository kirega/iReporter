"""
this file will include all the view endpoints for the application.
"""

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import User, IncidentModel

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


class SignUpEndpoint(Resource):
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


class LoginEndpoint(Resource):
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


class BaseIncidentEndpoint(Resource, IncidentModel):
    def __init__(self):
        self.db = IncidentModel()
        self.userdb = user_db
    # used to find a particular incident record

    def search(self, incidentId):
        return next(filter(lambda i: i["incidentId"] == incidentId, self.db.db), None)

    def search_user(self,userid):
        return next(filter(lambda u: u.userid == userid, self.userdb), None)

class AllIncidentsEndpoint(BaseIncidentEndpoint):
    """
        This endpoint handles the GET to get all incidents
        As well as POST for any new incident
    """

    def get(self):
        return make_response(jsonify(self.db.db), 200)

    def post(self):
        data = request.get_json(force=True)
        required_fields = ["incidentType", "comment",
                           "location", "createdBy", "images", "videos"]

        if all(i in data for i in required_fields):
            # Find the record created by a particular user
            result = next(filter(lambda u: u.userid ==
                                 data['createdBy'], self.userdb), None)
            if result is not None:
                new_incident = self.db.save(data['incidentType'], data["comment"], data['location'],
                                            data['createdBy'], data['images'], data['videos'])
                return make_response(jsonify({"message": "New incident created", "data": new_incident}), 201)
            else:
                return make_response(jsonify({"message": "Not Authorized"}), 401)

        else:
            return make_response(jsonify({"message": "Missing or invalid field members"}), 400)


class IncidentEndpoint(BaseIncidentEndpoint):

    def get(self, incidentId):
        if(len(self.db.db) > 0):
            result = self.search(incidentId)
            if result is not None:
                return make_response(jsonify({"data": result}), 200)
            else:
                return make_response(jsonify({"message": "Incident does not exist"}), 404)
        else:
            return make_response(jsonify({"message": "No incidents created yet!"}), 200)

    def delete(self, id):
        pass


class IncidentEditCommentEndpoint(BaseIncidentEndpoint):
    def put(self, incidentId):
        data = request.get_json(force=True)
        if len(data) > 0:
            result = self.search(incidentId)
            if result is not None:
                if result['status'] == 'draft':
                    if 'comment' in data and 'userid' in data :
                        user =  self.search_user(data['userid'])
                        if user is not None and user.userid == result['createdBy']:
                            result['comment'] = data['comment']
                            return make_response(jsonify({'message': "Incident Updated", "data":result}), 200)
                        else:
                            return make_response(jsonify({"message":"Forbidden: Record not owned"}), 403)
                    else:
                        return make_response(jsonify({"message":"Comment/userid is not present"}), 400)
                else:
                    return make_response(jsonify({"message":"Cannot update a record not in draft state"}),403)
            else:
                return make_response(jsonify({"message":"Update on non-existing record denied"}),404)
        else:
            return make_response(jsonify({"message": "Empty payload"}), 400)       

class IncidentEditLocationEndpoint(BaseIncidentEndpoint):
    def put(self, incidentId):
        data = request.get_json(force=True)
        if len(data) > 0:
            result = self.search(incidentId)
            if result is not None:
                if result['status'] == 'draft':
                    if 'location' in data and 'userid' in data:
                        user =  self.search_user(data['userid'])
                        if user is not None and user.userid == result['createdBy']:
                            result['location'] = data['location']
                            return make_response(jsonify({'message': "Incident Updated", "data":result}), 200)
                        else:
                            return make_response(jsonify({"message":"Forbidden: Record not owned"}), 403)
                    else:
                        return make_response(jsonify({"message":"Location/userid is not present"}), 400)
                else:
                    return make_response(jsonify({"message":"Cannot update a record not in draft state"}),403)
            else:
                return make_response(jsonify({"message":"Update on non-existing record denied"}),404)
        else:
            return make_response(jsonify({"message": "Empty payload"}), 400)       
