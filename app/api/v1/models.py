""""This file will contain all the models """
import datetime


class User():
    """User Model: it describes the behaviours and properties of a user"""

    def __init__(self, userid, first_name, last_name, other_names, phonenumber,
                 email, username, password, isAdmin=False, registeredOn=datetime.datetime.now()):
        self.userid = userid
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.phonenumber = phonenumber
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.registeredOn = registeredOn

    def __str__(self):
        return '{} {} {}'.format(self.userid, self.username, self.isAdmin)


incidents = [
    {
        "incidentId": 1,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "incidentType": "red-flag",
        "location": "1.323,-2.32",
        "status": "draft",
        "comment": "Police taking a bribe",
        "images": ['https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?cs=srgb&dl=beach-exotic-holiday-248797.jpg&fm=jpg'],
        "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"]
    },
    {
        "incidentId": 2,
        "createdOn": datetime.datetime.now(),
        "createdBy": 2,
        "incidentType": "intervention",
        "location": "1.323,-2.32",
        "status": "under-investigation",
        "comment": "Many potholes causing accidents",
        "images": [],
        "videos": []
    },
    {
        "incidentId": 3,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "incidentType": "red-flag",
        "location": "-1.28333, 36.81667",
        "status": "resolved",
        "comment": "once upon a time",
        "images": [],
        "videos": []
    }
]



class IncidentModel():
    def __init__(self):
        self.db = incidents

    def save(self, incidentType, comment, location, createdBy, images, videos, status="draft"):
        data = {
            "incidentId": len(self.db) + 1,
            "createdOn": datetime.datetime.now(),
            "createdBy": createdBy,
            "incidentType": incidentType,
            "location": location,
            "status": status,
            "comment": comment,
            "images": images,
            "videos": videos
        }
        self.db.append(data)
        return data