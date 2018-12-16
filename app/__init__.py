from flask import Flask, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

#local imports
from .v2 import api_version_two

def create_app():
	app = Flask(__name__)
	app.register_blueprint(api_version_two)

	@app.errorhandler(403)
	def forbidden(error):
		return make_response(jsonify({
			"Message" : "Forbidden"
			}),403)

	@app.errorhandler(404)
	def forbidden(error):
		return make_response(jsonify({
			"Message" : "Method not Allowed"
			}),404)

	@app.errorhandler(500)
	def forbidden(error):
		return make_response(jsonify({
			"Message" : "Server error"
			}),500)

	@app.errorhandler(405)
	def forbidden(error):
		return make_response(jsonify({
			"Message" : "Method not Allowed"
			}),405)
	return app

app = create_app()
	