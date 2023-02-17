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


    def get_ram(self, q=None):
        collection = self.get_db().ram

        return self.searchbar_query(collection, q)
            
    def get_cpu(self, q=None): #q is an optional argument
        collection = self.get_db().cpu

        return self.searchbar_query(collection, q)
    
    def get_gpu(self, q=None):
        collection = self.get_db().gpu 
        return self.searchbar_query(collection,q)
    
    def get_motherboard(self, q=None):
        collection = self.get_db().motherboard
        return self.searchbar_query(collection, q)

    def get_ssd(self, q=None):
        collection = self.get_db().ssd
        return self.searchbar_query(collection, q)
    
    def get_everything(self, q=None):        
        gpu = self.get_gpu(q)
        cpu = self.get_cpu(q)
        mb = self.get_motherboard(q)
        ram = self.get_ram(q)
        ssd = self.get_ssd(q)

        l = list(gpu + cpu + mb + ram + ssd)
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
    
    def get_ram(self, q=None): #q is an optional argument
        collection = self.get_db().ram

        return self.searchbar_query(collection, q)

    def get_ssd(self, q=None): #q is an optional argument
        collection = self.get_db().ssd

        return self.searchbar_query(collection, q)
    
    def get_everything_buf(self, q=None):
        # REFACTORING REQUIRED !!
        gpu = self.get_gpu(q)
        cpu = self.get_cpu(q)
        mb = self.get_motherboard(q)
        ram = self.get_ram(q)
        ssd = self.get_ssd(q)

        gpu = list(map(lambda x : {"name" : x["name"], "type" : "GPU", "price" : x["price"]}, gpu))
        cpu = list(map(lambda x : {"name" : x["name"], "type" : "CPU",  "price" : x["price"]}, cpu))
        mb = list(map(lambda x : {"name" : x["name"], "type" : "Scheda Madre",  "price" : x["price"]}, mb))
        ram = list(map(lambda x : {"name" : x["name"], "type" : "RAM",  "price" : x["price"]}, ram))
        ssd = list(map(lambda x : {"name" : x["name"], "type" : "SSD",  "price" : x["price"]}, ssd))

        return list(cpu+gpu+mb+ram+ssd)

class FilterTableSearchInterface(TableSearchInterface):
    def filter(self, request_args):

        l = self.get_everything_buf()
        keys = request_args.keys()
        if 'part' in keys:
            print(request_args['part'])
            if request_args['part'] == "CPU":
                l = self.get_cpu()
            elif request_args['part'] == "GPU":
                l = self.get_gpu()
            elif request_args['part'] == "Scheda Madre":
                l = self.get_motherboard()
            elif request_args['part'] == "RAM":
                l = self.get_ram()
            elif request_args['part'] == "SSD":
                l = self.get_ssd()

        if 'priceMin' in keys:
            print(request_args['priceMin'])
            if len(l) > 0:
                l = list(filter(lambda e : e["price"] > request_args['priceMin'], l))
        if 'priceMax' in keys:
            print(request_args['priceMax'])
            if len(l) > 0:
                l = list(filter(lambda e : e["price"] < request_args['priceMax'], l))
        
        return l

