from pymongo import (
    MongoClient,
    errors,
)
from pymongo import ASCENDING
import json

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
        _filter = {'_id' : 1}
        l = list(map(lambda e : e['_id'], collection.find(query, _filter))) 
        # print(collection.name)

        return self.searchbar_filter(l, q)
    
    def searchbar_filter(self, input, q):
        if isinstance(q, str) and q != '' and len(input) > 0:
            ll = list(filter( lambda i : q in i  ,input))
            # filter for elements that match the request arguments
            #i.e if q='amd ryzen', shows only amd ryzen cpu 
            return ll
        else:
            return input


    def get_cpu(self, q=None): #q is an optional argument
        collection = self.get_db().cpu

        return self.searchbar_query(collection, q)
    
    def get_gpu(self, q=None):
        collection = self.get_db().gpu 
        return self.searchbar_query(collection,q)
    
    def get_motherboard(self, q=None):
        collection = self.get_db().motherboard
        return self.searchbar_query(collection, q)
    
    def get_everything(self, q=None):
        gpu = self.get_gpu(q)
        cpu = self.get_cpu(q)
        mb = self.get_motherboard(q)

        l = list(gpu + cpu + mb)
        return l
    

class TableSearchInterface(PymongoInterface):
    def searchbar_query(self, collection, q):
        # We only need a few camps from the bson query result of 
        query = {}
        _filter = {'_id' : 1, 'price' : 1}
        l = list(map(lambda e : { 'name' : e['_id'], 'price' : e['price']['$numberInt'] }, collection.find(query, _filter).sort("price", ASCENDING))) 
        # the .sort() function in pymongo module sorts the list by price

        # print(collection.name)

        return self.searchbar_filter(l, q)
    
    def searchbar_filter(self, input, q):
        if isinstance(q, str) and q != '' and len(input) > 0:
            ll = list(filter( lambda i : q in i['name']  ,input))
            # filter for elements that match the request arguments
            #i.e if q='amd ryzen', shows only amd ryzen cpu 
            return ll
        else:
            return input


    def get_cpu(self, q=None): #q is an optional argument
        collection = self.get_db().cpu

        return self.searchbar_query(collection, q)
    
    def get_gpu(self, q=None):
        collection = self.get_db().gpu 
        return self.searchbar_query(collection,q)
    
    def get_motherboard(self, q=None):
        collection = self.get_db().motherboard
        return self.searchbar_query(collection, q)
    
    def get_everything_buf(self, q=None):
        # REFACTORING REQUIRED !!
        gpu = self.get_gpu(q)
        cpu = self.get_cpu(q)
        mb = self.get_motherboard(q)

        gpu = list(map(lambda x : {"name" : x["name"], "type" : "GPU", "price" : x["price"]}, gpu))
        cpu = list(map(lambda x : {"name" : x["name"], "type" : "CPU",  "price" : x["price"]}, cpu))
        mb = list(map(lambda x : {"name" : x["name"], "type" : "Scheda Madre",  "price" : x["price"]}, mb))

        return list(cpu+gpu+mb)

class FilterTableSearchInterface(TableSearchInterface):
    def filter(self, request_args):

        keys = request_args.keys()
        if 'part' in keys:
            print(request_args['part'])
        if 'priceMin' in keys:
            print(request_args['priceMin'])
        if 'priceMax' in keys:
            print(request_args['priceMax'])
        
        l = self.get_everything_buf()
        return l

