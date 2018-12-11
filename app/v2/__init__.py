from flask import Blueprint
from flask_restful import Api, Resource

from .incidents.views import RedFlags, RedFlag
from .users.views import UserSignup, UserSignin

api_version_two = Blueprint('v2', __name__, url_prefix="/v2")
api = Api(api_version_two)


api.add_resource(RedFlags, "/redflags")
api.add_resource(RedFlag, "/redflags/<int:num>")
api.add_resource(UserSignup, "/auth/signup")
api.add_resource(UserSignin, "/auth/login")