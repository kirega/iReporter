from flask import make_response,jsonify
from flask_restful import Resource

users = ['Peter','Mary']

class User(Resource):
    def __init__(self):
        self.users = users

    def get(self):
        return make_response(jsonify(self.users), 200)