from flask_restful import Resource
from flask import jsonify, make_response, request

from .models import IncidentsModel



class RedFlags(Resource, IncidentsModel):
	

	def __init__(self):
		self.db = IncidentsModel()

	def post(self):

		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return "Authorization header neede", 400

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if user[1] == True:
			data=request.get_json()
			createdBy=user[0]
			typee=data['type']
			location=data['location']
			status=data['status']
			images=data['images']
			videos=data['videos']

			resp = self.db.save(createdBy, typee, location, status, images, videos)

			return make_response(jsonify(
				{
				"Message" : "RedFlag has been created",
				"status" : 201
				}), 201)
		else:
			return "Not Authorized"

	def get(self):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return "Authorization header needed", 400

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if user[1] == True:
			resp = self.db.getallincidents()
			return make_response(jsonify(
						{
						"RedFlag" : resp,
						"status" : 200
						}), 200)
		else:
			return "Not Authorized"

class RedFlag(Resource, IncidentsModel):
	"""docstring for RedFlag"""
	def __init__(self):
		self.db = IncidentsModel()

	def get(self, num):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return "Authorization header needed", 400

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if user[1] == True:
			resp = self.db.getspecificincident(num)

			return make_response(jsonify(
				{
				"RedFlag" : resp,
				"status" : 201
				}), 201)
		else:
			return "Not Authorized"



		
