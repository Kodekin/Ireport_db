from flask_restful import Resource
from flask import jsonify, make_response, request

from .models import UsersModel



def _validator(user):
	error = False
	for key, value in user.items():
		if not value:
			error =  make_response(jsonify({
					"Error" : "Bad Request, {} is lacking".format(key)
					}), 403)
			return error

		if key == "username" or key =="password":
			if len(value) < 5:
				error =  make_response(jsonify({
					"Error" : "Bad Request, {} value is too short".format(key)
					}), 403)
			else:
				if len(value) > 20:
					error =  make_response(jsonify({
						"Error" : "Bad Request, {} value is too long".format(key)
						}), 403)
			return error
			
		if key == "email":
			if len(value) < 7:
				error =  make_response(jsonify({
						"Error" : "Bad Request, {} has bad format".format(key)
						}), 403)
				return error	
			else:
	 			if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
		 				return True
 				
			

			
class UserSignup(Resource):
	

	def post(self):
		data=request.get_json()

		user = dict(
			firstname=data['firstname'],
			lastname=data['lastname'],
			email=data['email'],
			username=data['username'],
			password=data['password']
		)

		valid = _validator(user)

		if valid == False:
			
			resp = UsersModel().save(user['firstname'], user['lastname'], user['email'], user['username'], user['password'])
			token = UsersModel().encode_auth_token(resp)
			return make_response(jsonify(
				{
				"Message" : "Success",
				"Auth-token" : token,
				"username" : resp, 
				"status" : 201
				}), 201)
		else:
			return valid

class UserSignin(Resource):
	


	def post(self):
		data=request.get_json()
		username=data['username']
		password=data['password']
		
		record = UsersModel().user_exists(username)
		if not record:
			return "No such user"
		username, passworddb = record
		if password == passworddb:
			token = UsersModel().encode_auth_token(username)
			return make_response(jsonify({
				"Message" : "Success",
				"Auth-token" : token,
				"user" : username
				}), 202)
		else:
			return "username/password do not match"
