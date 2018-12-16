from flask_restful import Resource
from flask import jsonify, make_response, request

from .models import UsersModel
import re
import string



def _validator(user):
	error = False

	for key, value in user.items():
		if not value:
			error =  make_response(jsonify({
					"Error" : "Hello user, {} field is required".format(key)
					}), 400)
			return error

		elif key == "username" or key == "password":
			if len(value.strip()) == 0:
				error =  make_response(jsonify({
					"Error" : "Hello user, {} field  is required".format(key)
					}), 400)
				return error

			if len(value) < 5:
				error =  make_response(jsonify({
					"Error" : "Hello user, {} value is too short".format(key)
					}), 400)
				return error
			
			elif len(value) > 20:
				error =  make_response(jsonify({
					"Error" : "Hello user, {} value is too long".format(key)
					}), 400)
				return error

			
		elif key == "email":
			if len(value) < 7 or  "@" not in value:
				error =  make_response(jsonify({
						"Error" : "Hello user, {} has bad format".format(key)
						}), 400)
				return error


		elif key == "firstname" or key == "lastname" :
			for i in value:

				if i not in string.ascii_letters:
					error =  make_response(jsonify({
						"Error" : "Field {} cannot take non-alphabetic characters".format(key),
						"status": 400
						}),400)
					return error



	else:
		return False

	
			

			
class UserSignup(Resource):
	

	def post(self):
		data=request.get_json()


		user = dict(
			firstname=data.get('firstname'),
			lastname=data.get('lastname'),
			email=data.get('email'),
			username=data.get('username'),
			password=data.get('password'),
			isadmin=data.get('isadmin')
		)

		valid = _validator(user)

		if valid == False:
			record = UsersModel().user_exists(user['username'])
			if record:
				return make_response(jsonify(
				{
				"Message" : "User already exist",
				"status" : 200
				}), 200)
			
			resp = UsersModel().save(user['firstname'], user['lastname'], user['email'], user['username'], user['password'], user['isadmin'])
			token = UsersModel().encode_auth_token(resp, user['isadmin'])
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
			return make_response(jsonify({
				"Message" : "No such user",
				"status" : 202
				}), 202) 

		username, passworddb, role = record
		if password == passworddb:
			token = UsersModel().encode_auth_token(username, role)
			return make_response(jsonify({
				"Message" : "User logged in successfully",
				"Auth-token" : str(token),
				"user" : str(username)
				}), 202)
		else:
			return make_response(jsonify({
				"Message" : "username/password do not match",
				"status" : 401
				}),401)

class UserLogOut(Resource):

	def post(self):
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return make_response(jsonify({
				"Message" : "Authorization header needed",
				"status" : 400
				}),400)

		token = auth_header.split(" ")[1]
		user = UsersModel().decode_auth_token(token)
		if not isinstance(user[0], int):
			resp =UsersModel().logout_user(token)
			if resp:
				return make_response(jsonify({
					"Message" : "successfully logged out",
					"status" : 201
					}),201)
		else:
			return make_response(jsonify({
				"Message" : "Not Authorized",
				"status" : 401
				}),401)		
