"""This file contains the create_app function which is a factory
for creating the app
"""
from flask import Flask 
from flask_restful import Api

# Local imports
from .api.v1.views import User

def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(User,'/users')
    return app

