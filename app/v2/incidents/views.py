from flask_restful import Resource
from flask import jsonify, make_response, request

from .models import IncidentsModel

def i_validator(incident):
	error = False

	for key, value in incident.items():
		if not value:
			error =  make_response(jsonify({
					"Error" : "Hello user, {} field is required".format(key)
					}), 400)
			return error

		elif key == "type" :
			if value != "RedFlag" or value != "Intervention":
				error =  make_response(jsonify({
					"Error" : "{} can only be either RedFlag or Intervention".format(key)
					}), 400)
				return error

		else:
			return False



class RedFlags(Resource, IncidentsModel):
	def __init__(self):
		self.db = IncidentsModel()

	def post(self):

		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return make_response(jsonify({
				"Message" : "Authorization header needed",
				"status" : 400
				}),400)

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if not isinstance(user[0], int):
			data=request.get_json()

			record=dict(
				createdBy=user[0],
				typee=data.get('type'),
				location=data.get('location'),
				description=data.get('description'),
				images=data.get('images'),
				videos=data.get('videos')
			)

			valid = i_validator(record)

			if valid == False:
				resp = self.db.save(record['createdBy'], record['typee'], record['location'], record['description'], record['images'], record['videos'])

				return make_response(jsonify(
					{
					"Incident" : resp,
					"Message" : "Incident has been created",
					"status" : 201
					}), 201)
			else:
				return valid

		else:
			return make_response(jsonify({
				"Message" : "Not Authorized",
				"status" : 401
				}),401)	

	def get(self):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return make_response(jsonify({
				"Message" : "Authorization header needed",
				"status" : 400
				}),400)

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if not isinstance(user[0], int):
			resp = self.db.getallincidents()
			return make_response(jsonify(
						{
						"RedFlag" : resp,
						"status" : 200
						}), 200)
		else:
			return make_response(jsonify({
				"Message" : "Not Authorized",
				"status" : 401
				}),401)	

class RedFlag(Resource, IncidentsModel):
	"""docstring for RedFlag"""
	def __init__(self):
		self.db = IncidentsModel()

	def get(self, incident_id):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return make_response(jsonify({
				"Message" : "Authorization header needed",
				"status" : 400
				}),400)

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if not isinstance(user[0], int):
			resp = self.db.getspecificincident(incident_id)
			return make_response(jsonify(
				{
				"RedFlag" : resp,
				"status" : 201
				}), 201)
		else:
			return make_response(jsonify({
				"Message" : "Not Authorized",
				"status" : 401
				}),401)	

	def put(self, incident_id):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return make_response(jsonify({
				"Message" : "Authorization header needed",
				"status" : 400
				}),400)

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if not isinstance(user[0], int):
			_owner = IncidentsModel().record_exists(incident_id)
			if not _owner:
				return make_response(jsonify(
					{
					"Message" : "Item does not exist",
					"status" : 404
					}), 404)
			_id, n_owner = _owner
			email = IncidentsModel().get_owner_email(n_owner)
			if user[0] == n_owner or user[1] == "True":

				req_data = request.get_json()
				update = req_data.items()
				for field, data in update:
					#Admin only operation
					if field == "status":
						if user[1] == "True":
							resp = self.db.update_item(field, data, incident_id)
							body = "Hey <b>{}</b>,</ br> the status of your incident has been changed to <b><i>{}</i></b>".format(n_owner, data)
							IncidentsModel().send_email(email, body)
							msg = "{} updated successfully".format(resp)

							return make_response(jsonify(
								{
								"Attribute" : resp,
								"Message" : msg,
								"status" : 200
								}), 200)
						else:
							return make_response(jsonify({"Message" : "Unauthorzed operation - Admin only", "status" : 401}), 401)

					resp = self.db.update_item(field, data, incident_id)
					msg = "{} updated successfully".format(resp)

					return make_response(jsonify(
						{
						"Attribute" : resp,
						"Message" : msg,
						"status" : 200
						}), 200)
			else:
				return make_response(jsonify(
					{
					"Message" : "Unauthorzed operation cannot edit this item",
					"status" : 401
					}), 401)

		else:
			return make_response(jsonify({
				"Message" : "Not Authorized",
				"status" : 401
				}),401)	

	def delete(self, incident_id):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return make_response(jsonify({
				"Message" : "Authorization header needed",
				"status" : 400
				}),400)

		token = auth_header.split(" ")[1]
		user = IncidentsModel().decode_auth_token(token)

		if not isinstance(user[0], int):
			_owner = IncidentsModel().record_exists(incident_id)
			if not _owner:
				return make_response(jsonify(
					{
					"Message" : "Item does not exist",
					"status" : 404
					}), 404)

			_id, n_owner = _owner
			if user[0] == n_owner:
				resp = self.db.destroy(incident_id)
				msg = "Id {} deleted successfully".format(resp)

				return make_response(jsonify(
					{
					"Message" : msg,
					"status" : 200
					}), 200)
			else:
				return make_response(jsonify(
					{
					"Message" : "Unauthorzed operation cannot delete this item",
					"status" : 401
					}), 401)

		else:
			return make_response(jsonify({
				"Message" : "Not Authorized",
				"status" : 401
				}),401)	


	
		



		
