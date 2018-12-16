from app.db_config import init_db
import time, datetime
from ..base_model import BaseClassModel




class IncidentsModel(BaseClassModel):

    def __init__(self):

        self.db = init_db()


    def save(self, createdBy, typee, location, description, images, videos):
        payload = {
            "createdBy": createdBy,
            "typee": typee,
            "location": location,
            "status": "draft",
            "description": description,
            "images": images,
            "videos": videos,
        }

        query = """INSERT INTO incidents (createdBy, type, location, status, description, images, videos) VALUES
                    (%(createdBy)s, %(typee)s, %(location)s, %(status)s, %(description)s, %(images)s, %(videos)s) RETURNING incident_id """
        curr = self.db.cursor()
        curr.execute(query, payload)
        incident_id =  curr.fetchone()[0]
        self.db.commit()
        return incident_id



    def getallincidents(self):
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT incident_id, createdBy, type, location, status, description, images, videos, createdOn FROM incidents;""")
        data = curr.fetchall()
        resp = []
        for i, records in enumerate(data):
           incident_id, createdBy, typee, location, status, description, images, videos, createdOn = records
           info = dict(
                incident_id=int(incident_id),
                createdBy=str(createdBy),
                typee=str(typee),
                location=str(location),
                status=str(status),
                description=str(description),
                images=str(images),
                videos=str(videos),
                createdOn=str(createdOn)
                )

           resp.append(info)
        return resp

    def getspecificincident(self, incident_id):
        _record = self.record_exists(incident_id)
        if not _record:
            return "Record does not exists"
        else:
            curr = self.db.cursor()
            query = "SELECT incident_id, createdBy, type, location, status, description, images, videos, createdOn FROM incidents WHERE incident_id={};".format(incident_id)
            curr.execute(query)
            data = curr.fetchone()
            resp = []
            info = dict(
                incident_id=data[0],
                createdBy=data[1],
                type=str(data[2]),
                location=str(data[3]),
                status=str(data[4]),
                description=str(data[5]),
                images=str(data[6]),
                videos=str(data[7]),
                createdOn=str(data[8])
            )
            resp.append(info)

            return resp

    def get_specific_user_incident(self, username):
        dbconn = self.db
        curr = dbconn.cursor()
        query = "SELECT incident_id, type, location, status, description, images, videos, createdOn FROM incidents WHERE createdBy='{}';".format(username)
        curr.execute(query)
        data = curr.fetchall()
        resp = []
        for i, records in enumerate(data):
           incident_id, typee, location, status, description, images, videos, createdOn = records
           info = dict(
                incident_id=int(incident_id),
                typee=str(typee),
                location=str(location),
                status=str(status),
                description=str(description),
                images=str(images),
                videos=str(videos),
                createdOn=str(createdOn)
                )

           resp.append(info)
        return resp

    def update_item(self, field, data, incident_id):
        curr = self.db.cursor()
        update = "UPDATE incidents SET {}='{}' WHERE incident_id={};".format(field, data, incident_id)
        curr.execute(update)
        self.db.commit()
        return field


    def destroy(self, incident_id):
        curr = self.db.cursor()
        del_qry= "DELETE FROM incidents WHERE incident_id={};".format(incident_id)
        curr.execute(del_qry)
        self.db.commit()
        return incident_id

    def record_exists(self, incident_id):
        curr = self.db.cursor()
        query = "SELECT incident_id, createdBy FROM incidents WHERE incident_id='{}';".format(incident_id)
        curr.execute(query)
        return curr.fetchone()

    def get_owner_email(self, username):
        curr = self.db.cursor()
        query = "SELECT email FROM users WHERE username='{}';".format(username)
        curr.execute(query)
        return curr.fetchone()




   
