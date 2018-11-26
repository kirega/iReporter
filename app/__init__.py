"""This file contains the create_app function which is a factory
for creating the app
"""
from flask import Flask 
from flask_restful import Api

# Local imports
from .api.v1 import v1

def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1)
    return app

