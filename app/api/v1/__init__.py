from flask import Blueprint
from flask_restful import Api
from .views import User

v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api =  Api(v1)
api.add_resource(User,'/users')

