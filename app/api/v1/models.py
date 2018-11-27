""""This file will contain all the models """


class User():
    """User Model: it describes the behaviours and properties of a user"""

    def __init__(self, first_name, last_name, other_names, phonenumber,
                 email, username, password, isAdmin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.phonenumber = phonenumber
        self.email = email
        self.password = password
        self.isAdmin = isAdmin