import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app
from ...db_config import _init_db
from ...db_config import destroy_tables


class AuthTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.user = {
                "firstname" : "mwakidusa",
                "lastname" : "tommwasaka",
                "email" : "tom@gmail.com",
                "username" : "hosanssasadqw",
                "password" : "dhfjfjjs",
                "isadmin" : True
            }
        with self.app.app_context():
            self.db = _init_db()

    def post_data(self, path='/v2/auth/signup', data={}):
        if not data:
            data = self.user
        result = self.client.post(path, data=json.dumps(data),
                                  content_type='application/json')
        return result

    def user_login(self, path='/v2/auth/login', data={}):
        self.post_data(data=self.user)
        payload = {
            "username": self.user['username'],
            "password": self.user['password']
        }
        result = self.client.post(path, data=json.dumps(payload), content_type='application/json')
        return result

    def logout_user(self, path='/v2/auth/logout', data={}):
        new_user = self.post_data()
        token = new_user.json['Auth-token']
        headers = {"Authorization": "Bearer {}".format(token)}
        result = self.client.post(path, data="", headers=headers,
                                  content_type='application/json')
        return result

    def test_sign_up_user(self):
        new_user = self.post_data()
        self.assertEqual(new_user.status_code, 201)
        self.assertTrue(new_user.json["Auth-token"])

    def test_user_login(self):
        reg = self.post_data()
        login = self.user_login()
        self.assertEqual(login.json["Message"], "User logged in successfully")
        self.assertEqual(login.status_code, 202)
        self.assertTrue(login.json["Auth-token"])

    def test_empty_string_field(self):
        payload = {
            "firstname" : "jdkandlals",
            "lastname" : "markobed",
            "email" : "tom@gmail.com",
            "username" : "toskask",
            "password" : "",
            "isadmin" : True
        }
        empty_req = self.client.post(path='/v2/auth/signup', data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(empty_req.status_code, 400)
        self.assertEqual(empty_req.json['Error'], "Hello user, password field is required")

    def test_length_of_credentials(self):
        payload = {
            "firstname" : "jdkandlals",
            "lastname" : "emery",
            "email" : "tom@gmail.com",
            "username" : "tos",
            "password" : "dhfjfjjs",
            "isadmin" : True

        }
        short_req = self.client.post(path='/v2/auth/signup', data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(short_req.status_code, 400)
        self.assertEqual(short_req.json['Error'], "Hello user, username value is too short")

    def test_email_format(self):
        payload = {
            "firstname" : "jdkandlals",
            "lastname" : "emery",
            "email" : "tomgmail.com",
            "username" : "tommwaka",
            "password" : "dhfjfjjs",
            "isadmin" : True
        }
        mail = self.client.post(path='/v2/auth/signup', data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(mail.status_code, 400)
        self.assertEqual(mail.json['Error'], "Hello user, email has bad format")

    def test_string_characters(self):
        payload = {
            "firstname" : "576483",
            "lastname" : "emery",
            "email" : "tom@gmail.com",
            "username" : "tommwaka",
            "password" : "dhfjfjjs",
            "isadmin" : True
        }
        value_typ = self.client.post(path='/v2/auth/signup', data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(value_typ.status_code, 400)
        self.assertEqual(value_typ.json['Error'], "Field firstname cannot take non-alphabetic characters")


    def test_an_unregistered_user(self):
        un_user = {
            "username": "hakdkasjdhjaksod",
            "password": "12231031230231"
            }
        
        login = self.client.post(path='/v2/auth/login', data=json.dumps(un_user), content_type='application/json')
        self.assertEqual(login.json['Message'], "No such user")

    def test_missing_field(self):
        payload = {
            "lastname" : "emery",
            "email" : "tom@gmail.com",
            "username" : "tommwaka",
            "password" : "dhfjfjjs",
            "isadmin" : True
        }
        no_field = self.client.post(path='/v2/auth/signup', data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(no_field.status_code, 400)
        self.assertEqual(no_field.json['Error'], "Hello user, firstname field is required")

    def test_user_logout(self):
        logout = self.logout_user()
        self.assertEqual(logout.json["Message"], "successfully logged out")
        self.assertEqual(logout.status_code, 201)

    def tearDown(self):

        with self.app.app_context():
            destroy_tables()
            self.db.close()


if __name__ == "__main__":
    unittest.main()