from flask import Flask, Blueprint
from flask_restful import Api, Resource
from .db_config import create_tables

#local imports
from .v2 import api_version_two

def create_app():
	app = Flask(__name__)
	create_tables()
	app.register_blueprint(api_version_two)
	return app
	