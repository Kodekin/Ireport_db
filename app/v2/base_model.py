from datetime import datetime, timedelta
import jwt
import os

from app.db_config import init_db

class BaseClassModel(object):
	"""docstring for BaseClassModel"""
	def __init__(self):
		self.db = init_db()

	@staticmethod
	def encode_auth_token(username):
		try:
			payload = {
			"exp": datetime.utcnow() + timedelta(days=1),
			"iat": datetime.utcnow(),
			"sub": username
            }
			token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
			resp = token.decode("utf-8")
		except Exception as e:
			resp = e
		return resp

	def blacklisted(self, token):
		dbconn = self.db
		curr = dbconn.cursor()
		query = """
                SELECT * FROM blacklist WHERE tokens = %s;
                """
		curr.execute(query, [token])
		if curr.fetchone():
			return True
		return False



	def decode_auth_token(self, auth_token):
		"""This function takes in an auth
		token and decodes it
		"""
		if self.blacklisted(auth_token):
			return "Token has been blacklisted"
		secret = os.getenv("SECRET_KEY")
		try:
			token = auth_token.encode("utf-8")
			payload = jwt.decode(token, secret)
			return [payload['sub'], True]  # user id
		except jwt.ExpiredSignatureError:
			return "The token has expired"
		except jwt.InvalidTokenError:
			return "The token is invalid"

