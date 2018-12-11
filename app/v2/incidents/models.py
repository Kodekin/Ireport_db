from app.db_config import init_db
import time, datetime
from ..base_model import BaseClassModel




class IncidentsModel(BaseClassModel):

    def __init__(self):

        self.db = init_db()


    def save(self, createdBy, typee, location, status, images, videos):
        payload = {
            "createdBy": createdBy,
            "typee": typee,
            "location": location,
            "status": status,
            "images": images,
            "videos": videos,
        }

        query = """INSERT INTO incidents (createdBy, type, location, status, images, videos) VALUES
                    (%(createdBy)s, %(typee)s, %(location)s, %(status)s, %(images)s, %(videos)s)"""
        curr = self.db.cursor()
        curr.execute(query, payload)
        self.db.commit()
        return payload



    def getallincidents(self):
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT incident_id, createdBy, type, location, status, images, videos, createdOn FROM incidents;""")
        data = curr.fetchall()
        resp = []
        for i, records in enumerate(data):
           incident_id, createdBy, typee, location, status, images, videos, createdOn = records
           info = dict(
                incident_id=int(incident_id),
                createdBy=str(createdBy),
                typee=str(typee),
                location=str(location),
                status=str(status),
                images=str(images),
                videos=str(videos),
                createdOn=str(createdOn)
                )

           resp.append(info)
           return resp

      def getspecificincident(self, num):
        
        curr = self.db.cursor()
        query = "SELECT incident_id, createdBy, type, location, status, images, videos, createdOn FROM incidents WHERE incident_id={};".format(num)
        curr.execute(query)
        data = curr.fetchone()
        resp = []
        info = dict(
            incident_id=data[0],
            createdBy=data[1],
            type=str(data[2]),
            location=str(data[3]),
            status=str(data[4]),
            images=str(data[5]),
            videos=str(data[6]),
            createdOn=str(data[7])
        )
        _record = self.record_exists(info['num'])
        if not _record:
            return "Record does not exists"
        else:
            resp.append(info)

            return resp


   
