from flask_login import UserMixin

from controller.pymongo_interface import PymongoInterface
from pymongo.errors import DuplicateKeyError
import yaml

config = yaml.safe_load(open("config.yml"))

CONNECTION_STRING = config["mongodb"]

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        pi = PymongoInterface(CONNECTION_STRING)
        db = pi.get_db().user

        try:
            user = db.find_one({"_id" : user_id})
        except Exception as e:
            return None

        if user == None:
            return None
        
        try:
            user = User(user["_id"], user["name"], user["email"], user["profile_pic"] )
        except TypeError as e:
            return None
    
        pi.close()
        return user 

    @staticmethod
    def create(id_, name, email, profile_pic):
        pi = PymongoInterface(CONNECTION_STRING)
        db = pi.get_db().user 

        doc = {"_id" : id_, "name" : name,  "email" : email, "profile_pic" : profile_pic }
        try:
            db.insert_one(doc)
        except DuplicateKeyError as e:
            print(e)
        pi.close()
