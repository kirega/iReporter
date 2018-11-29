from flask import Blueprint
from flask_restful import Api
from .views import (SignUpEndpoint, LoginEndpoint,
                    AllIncidentsEndpoint, IncidentEndpoint,
                    IncidentEditCommentEndpoint, IncidentEditLocationEndpoint)

v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(v1)
api.add_resource(SignUpEndpoint, '/signup')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(AllIncidentsEndpoint, '/incidents')
api.add_resource(IncidentEndpoint, '/incident/<int:incidentId>')
api.add_resource(IncidentEditCommentEndpoint, '/incident/<int:incidentId>/comment')
api.add_resource(IncidentEditLocationEndpoint, '/incident/<int:incidentId>/location')
