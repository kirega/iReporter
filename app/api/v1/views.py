"""
this file will include all the view endpoints for the application.
"""

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import User, IncidentModel

from .validators import (UserSchema, IncidentSchema,
                         IncidentEditSchema)


class SignUpEndpoint(Resource, User):
    """
    A resource that provides the endpoint POST /signup.

    """

    def __init__(self):
        self.user = User()

    def post(self):
        """
        Registers new users based on data sent
        """
        data = request.get_json(force=True)
        user_data, error = UserSchema().load(data)

        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        if self.user.check_username(user_data['username']):
            return make_response(jsonify({"message": "Username already exists"}), 400)
        if self.user.check_email(user_data['email']):
            return make_response(jsonify({"message": "Email already exists"}), 400)

        if 'isAdmin' in user_data:
            self.user.save(
                user_data['first_name'],
                user_data['last_name'],
                user_data['other_names'],
                user_data['phonenumber'],
                user_data['email'],
                user_data['username'],
                user_data["password"],
                user_data['isAdmin']
            )
        else:
            self.user.save(
                user_data['first_name'],
                user_data['last_name'],
                user_data['other_names'],
                user_data['phonenumber'],
                user_data['email'],
                user_data['username'],
                user_data["password"]
            )

        return make_response(jsonify({"message": "Sign Up successful. Welcome!"}), 201)


class LoginEndpoint(Resource, User):
    """ This endpoints handles all login posts
    POST /login"""

    def __init__(self):
        self.users = User()

    def post(self):
        """ Accepts login credentials and return success on succcessful authentication"""

        data = request.get_json(force=True)
        user_data, error = UserSchema(
            only=('username', 'password')).load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.users.confirm_login(user_data['username'], user_data['password']):
            return make_response(jsonify({"message": "Login Success!"}), 200)

        return make_response(jsonify({"message": "Login Failed!"}), 401)


class BaseIncidentEndpoint(Resource, IncidentModel, User):
    """Base class for  ll derivative incidents resources"""

    def __init__(self):
        self.db = IncidentModel()
        self.user = User()


class AllIncidentsEndpoint(BaseIncidentEndpoint):
    """
        This endpoint handles the GET to get all incidents
        As well as POST for any new incident
    """

    def get(self):
        """Endpoint GET /incidents.
        Returns list of all incidents"""
        return make_response(jsonify(self.db.db), 200)

    def post(self):
        """Enpoint POST /incidents
        Allows creation of new incidents"""

        data = request.get_json(force=True)
        incident_data, error = IncidentSchema().load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.user.search_user(incident_data['createdBy']):
            new_incident = self.db.save(data['incidentType'], data["comment"], data['location'],
                                        data['createdBy'], data['images'], data['videos'])
            return make_response(jsonify({"message": "New incident created",
                                          "data": new_incident}), 201)

        return make_response(jsonify({"message": "Not Authorized"}), 401)


class IncidentEndpoint(BaseIncidentEndpoint):
    """"Endpoint for managing individual instance records"""

    def get(self, incident_id):
        """
        GET /incident/<incident_id>
        Returns a single instance
        """

        if self.db.db:
            result = self.db.search_incident(incident_id)
            if result is not None:
                return make_response(jsonify({"data": result}), 200)
            return make_response(jsonify({"message": "Incident does not exist"}), 404)

        return make_response(jsonify({"message": "No incidents created yet!"}), 200)

    def delete(self, incident_id):
        """
        DELETE /incident/<incident_id>
        deletes a single instance
        """

        data = request.get_json(force=True)
        incident_data = IncidentEditSchema(
            only=('userid',)).load(data)
        if incident_data.errors:
            return make_response(jsonify({
                "message": "Missing userid field",
                "required": incident_data.errors,
                "status": 400}), 400)
        result = self.db.search_incident(incident_id)

        if result is not None:
            user = self.user.search_user(data['userid'])
            if user is not None and user['userid'] == result['createdBy']:
                incident_to_pop = self.db.db.index(result)
                self.db.db.pop(incident_to_pop)
                return make_response(jsonify({
                    "message": "Incident record has been deleted",
                    "status": 204,
                    "id": incident_id}), 200)

            return make_response(jsonify({"message": "Forbidden: Record not owned",
                                          "status": 403}), 403)

        return make_response(jsonify({
            "message": "Incident does not exist",
            "status": 404
        }), 404)


class IncidentEditCommentEndpoint(BaseIncidentEndpoint):
    """
    Enpoint PUT /incident/1
    Allows for editing the comment on an incident
    """

    def put(self, incident_id):
        """Allows for editing the comment on an incident"""

        data = request.get_json(force=True)
        incident_data = IncidentEditSchema(
            only=('userid', 'comment')).load(data)
        if incident_data.errors:
            return make_response(jsonify({
                "message": "Comment/userid is not present",
                "required": incident_data.errors}),
                400)

        result = self.db.search_incident(incident_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['comment'] = data['comment']
                    return make_response(jsonify({
                        'message': "Incident Updated",
                        "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)


class IncidentEditLocationEndpoint(BaseIncidentEndpoint):
    """
    Enpoint PUT /incident/1
    Allows for editing the location on an incident
    """

    def put(self, incident_id):
        """  Allows for editing the location on an incident"""

        data = request.get_json(force=True)
        incident_data = IncidentEditSchema(
            only=('userid', 'location')).load(data)
        if incident_data.errors:
            return make_response(jsonify({
                "message": "location/userid is not present",
                "required": incident_data.errors}),
                400)
        result = self.db.search_incident(incident_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['location'] = data['location']
                    return make_response(jsonify({
                        'message': "Incident Updated", "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)
