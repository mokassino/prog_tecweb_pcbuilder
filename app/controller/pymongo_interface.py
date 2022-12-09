from pymongo import (
    MongoClient,
    errors
)

class PymongoInterface:
    def __init__(self, string):
        self.CONNECTION_STRING = string 
        self.client = MongoClient(string)
    def get_db(self):
        return self.client.pcbuilder
    def close(self):
        self.client.close()

