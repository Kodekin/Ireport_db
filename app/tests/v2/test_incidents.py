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
                "username" : "hsjakedlad",
                "password" : "dhfjfjjs",
                "isadmin" : True
            }
        self.redflag = {
              "type" : "redflag",
              "location" : "45E, 24N",
              "status" : "draft", 
              "images" : "image", 
              "description" : "description",
              "videos" : "video",
              "comment" : "whats happening.."
            }
        with self.app.app_context():
            self.db = _init_db()

    def create_user(self, data={}):
        if not data:
            data = self.user
        result = self.client.post('/v2/auth/signup', data=json.dumps(data),
                                  content_type='application/json')
        token = result.json['Auth-token']
        username = result.json['username']
        return username, token


    def create_incident(self, token=2, data={}):
        if token is 2:
            token = self.create_user()[1]
        if not data:
            data = self.redflag
        headers = {"Authorization": "Bearer {}".format(token)}
        result = self.client.post('/v2/redflags', data=json.dumps(data), headers=headers,
                                                content_type='application/json')
        return result

    def get_flags(self, path=''):
        if not path:
            path = '/v2/redflags'
        token = self.create_user()[1]
        headers = {"Authorization": "Bearer {}".format(token)}
        result = self.client.get(path, headers=headers, content_type='application/json')        
        return result

    def delete_incident(self):
        auth_token = self.create_user()[1]
        incident_id = int(self.create_incident(token=auth_token, data=self.redflag).json['Incident'])
        path = "/v2/redflags/{}".format(incident_id)
        headers = {"Authorization": "Bearer {}".format(auth_token)}
        result = self.client.delete(path, headers=headers, content_type='application/json')        
        return result

    def edit_flags(self):
        """Test that a user can edit incident that they have posted"""
        auth_token = self.create_user()[1]
        incident_id = int(self.create_incident(token=auth_token, data=self.redflag).json['Incident'])
        path = "/v2/redflags/{}".format(incident_id) 
        headers = {"Authorization": "Bearer {}".format(auth_token)}
        data = {"location": "edited location"}
        result = self.client.put(path, data=json.dumps(data), headers=headers, content_type='application/json')
        return result


    def test_post_incident(self):
        new_flag = self.create_incident()
        self.assertEqual(new_flag.status_code, 201)
        self.assertEqual(new_flag.json["Message"], "Incident has been created")

    def test_get_incidents(self):
        incidents = self.get_flags()
        self.assertEqual(incidents.status_code, 200)

    def test_get_specific_user_incidents(self):
        path = '/v2/redflags/{}'.format(self.user['username'])
        incidents = self.get_flags(path=path)
        self.assertEqual(incidents.status_code, 200)

    def test_edit_incident(self):
        """Test that users can edit an incident that they have posted"""
        incident = self.edit_flags()
        self.assertEqual(incident.status_code, 200)
        self.assertEqual(incident.json["Message"], "location updated successfully")

    def test_edit_if_not_item_owner(self):
        data = {
                "firstname" : "mwakidusa",
                "lastname" : "tommwasaka",
                "email" : "tom@gmail.com",
                "username" : "shakds",
                "password" : "dhfjfjjs",
                "isadmin" : "False"
        }
        user = self.client.post(path='/v2/auth/signup', data=json.dumps(data),
                                  content_type='application/json')
        token = user.json['Auth-token']
        new_incident = self.create_incident()
        incident_id = int(new_incident.json['Incident'])
        path = "/v2/redflags/{}".format(incident_id)
        headers = {"Authorization": "Bearer {}".format(token)}
        payload = {"status": "resolved"}
        result = self.client.put(path, data=json.dumps(payload), headers=headers, content_type='application/json')
        self.assertEqual(result.json["Message"], "Unauthorzed operation cannot edit this item")
        self.assertEqual(result.status_code, 401)


    def test_delete_incident(self):
        """Test that users can delete an incident that they have posted"""
        incident = self.delete_incident()
        self.assertEqual(incident.status_code, 200)
        self.assertEqual(incident.json["Message"], "Id 1 deleted successfully")


    def tearDown(self):

        with self.app.app_context():
            destroy_tables()
            self.db.close()


if __name__ == "__main__":
    unittest.main()