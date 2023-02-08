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
    def get_processors(self):
        return self.client.pcbuilder.processor
    def close(self):
        self.client.close()

class SearchBarInterface(PymongoInterface):
    def get_processors(self, q=None): #q is an optional argument
        # We don't need everything in the search bar so i'll made a filter
        query = {} # find everything
        _filter = {'_id' : 1, 'brand' : 1}

        p = self.client.pcbuilder.processor

        l = list(p.find(query, _filter))
        ll = list(map(lambda x : x['brand']+' '+ x['_id'], l)) # merge two camps from the json output into a list of strings
        # i.e:  {_id: "5 5600" , brand: "amd ryzen"} --becomes-->  "amd ryzen 5 5600"
        # then convert back to a list
        if q != None or q != '':
            ll = list(filter( lambda i : q in i  ,ll)) # filter for elements that match the request arguments
        #i.e if q='amd ryzen', shows only amd ryzen elements


        return ll #return a list of specific camps from a JSON

