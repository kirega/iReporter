""""This file will contain all the models """
import datetime

USER_DB = []


class User():
    """User Model: it describes the behaviours and properties of a user"""

    def __init__(self):
        self.db = USER_DB
        self.save(
            first_name="Joseph",
            last_name="Mutiga",
            other_names="Kirega",
            phonenumber="0716570355",
            email="kirega@gmail.com",
            username="kirega",
            password="1234",
            isAdmin=True
        )

    def save(self, first_name, last_name, other_names, phonenumber,
             email, username, password, isAdmin=False):
        """Method to save a new instance into the userdb"""

        data = {
            "userid": len(self.db) + 1,
            "first_name": first_name,
            "last_name": last_name,
            "other_names": other_names,
            "phonenumber": phonenumber,
            "username": username,
            "email": email,
            "password": password,
            "isAdmin": isAdmin,
            "registeredOn": datetime.datetime.now(),
        }
        self.db.append(data)
        return data

    def check_username(self, username):
        """Checks that the user exists"""
        return next(filter(lambda x: x['username'] == username, self.db), None)

    def check_email(self, email):
        """Checks that the user exists"""
        return next(filter(lambda x: x['email'] == email, self.db), None)

    def confirm_login(self, username, pwd):
        """Checks that both username and password are valid for login"""
        return next(filter(lambda x: x['username'] == username and x['password'] == pwd, self.db), None)

    def search_user(self, id):
        """"Utility function for  searching the existence of an user in the database"""
        return next(filter(lambda u: u['userid'] == id, self.db), None)


INCIDENTS = [
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
        self.db = INCIDENTS

    def save(self, incidentType, comment, location, createdBy, images, videos, status="draft"):
        uid = len(self.db) + 1
        data = {
            "incidentId": uid,
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

    def search_incident(self, id):
        """"Utility function for  searching the existence of an instance in the database"""
        return next(filter(lambda i: i["incidentId"] == id, self.db), None)
    
