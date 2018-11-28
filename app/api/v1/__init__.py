from flask import Blueprint
from flask_restful import Api
from .views import SignUp, Login, AllIncidents

v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api =  Api(v1)
api.add_resource(SignUp,'/signup')
api.add_resource(Login,'/login')
api.add_resource(AllIncidents,'/incidents')

