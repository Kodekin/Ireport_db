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
                "password" : "dhfjfjjs"
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

    def test_sign_up_user(self):
        new_user = self.post_data()
        self.assertEqual(new_user.status_code, 201)
        self.assertTrue(new_user.json["Auth-token"])

    def test_user_login(self):
        reg = self.post_data()
        login = self.user_login()
        self.assertEqual(login.json["Message"], "Success")
        self.assertEqual(login.status_code, 202)
        self.assertTrue(login.json["Auth-token"])

    def test_validation(self):
        payload = {
            "firstname" : "jdkandlals",
            "lastname" : "",
            "email" : "tom@gmail.com",
            "username" : "toskask",
            "password" : "dhfjfjjs"
        }
        empty_req = self.client.post(path='/v2/auth/signup', data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(empty_req.status_code, 403)
        self.assertEqual(empty_req.json['Error'], "Bad Request, lastname is lacking")


    def test_an_unregistered_user(self):
        un_user = {
            "username": "hakdkasjdhjaksod",
            "password": "12231031230231"
            }
        
        login = self.client.post(path='/v2/auth/login', data=json.dumps(un_user), content_type='application/json')
        self.assertEqual(login.json['Message'], "No such user")

    def tearDown(self):

        with self.app.app_context():
            destroy_tables()
            self.db.close()


if __name__ == "__main__":
    unittest.main()