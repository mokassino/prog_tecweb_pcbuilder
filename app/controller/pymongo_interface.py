from pymongo import (
    MongoClient,
    errors
)

class PymongoInterface:
    def __init__(self, string):
        self.CONNECTION_STRING = string 
        self.client = MongoClient(self.CONNECTION_STRING)
    def get_db(self):
        return self.client.pcbuilder
    def close(self):
        self.client.close()

class SearchBarInterface(PymongoInterface): #sub class of PymongoInterface
    def searchbar_query(self, collection, q):
        # We only need a few camps from the bson query result of 
        query = {}
        l = list()

        if collection.name == 'gpu' or collection.name == 'processor':
            _filter = {'_id' : 1, 'brand' : 1}
            l = list(map(lambda x : x['brand']+' '+ x['_id'], collection.find(query, _filter))) 
            # collection.find() make a query on the database with the _filter and returns stuff
            # the lambda function merges two camps from the json output and pass them to the map function
            # i.e:  {_id: "5-5600" , brand: "amd ryzen"} --becomes-->  "amd ryzen 5-5600" # then convert back to a list
        elif collection.name == 'motherboard':
            _filter = {'_id' : 1, 'name' : 1, 'brand' : 1, }
            l = list(map(lambda x : x['brand']+ ' '+ x['name'] + ' ' + x['_id'], collection.find(query, _filter))) 

        return self.searchbar_filter(l, q)
    
    def searchbar_filter(self, input, q):
        if (q is type("string")) and len(input) > 0:
            ll = list(filter( lambda i : q in i  ,input))
            # filter for elements that match the request arguments
            #i.e if q='amd ryzen', shows only amd ryzen cpu 
            return ll
        else:
            return input


    def get_processors(self, q=None): #q is an optional argument
        collection = self.get_db().processor

        return self.searchbar_query(collection, q)
    
    def get_gpu(self, q=None):
        collection = self.get_db().gpu 
        return self.searchbar_query(collection,q)
    
    def get_motherboard(self, q=None):
        collection = self.get_db().motherboard
        return self.searchbar_query(collection, q)
    
    def get_everything(self, q=None):
        gpu = self.get_gpu(q)
        cpu = self.get_processors(q)
        mb = self.get_motherboard(q)

        l = list(gpu + cpu + mb)
        return l

