from flask import Flask, Blueprint
from flask_restful import Api, Resource

#local imports
from .v2 import api_version_two

def create_app():
	app = Flask(__name__)
	app.register_blueprint(api_version_two)
	return app

app = create_app()
	