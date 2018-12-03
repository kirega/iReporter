"""This file contains the create_app function which is a factory
for creating the app
"""
from flask import Flask 
from flask_restful import Api
from instance import config
# Local imports
from .api.v1 import v1


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevelopmentConfig)
    app.register_blueprint(v1)
    return app

