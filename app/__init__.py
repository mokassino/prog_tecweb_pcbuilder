from flask import Flask, Blueprint
from flask_restful import Resource,Api, request
from app.controller import (
        main,
        pymongo_interface
    )
from bson.json_util import loads,dumps

api = Api(main.api_bp)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.register_blueprint(main.bp)
    app.register_blueprint(main.api_bp)

    return app

class SearchBar(Resource):
    def get(self):
        CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"
        l = pymongo_interface.SearchBarInterface(CONNECTION_STRING).get_processors()

        q = request.args['q']

        ll = list(filter( lambda i : args['q'] in i   ,l)) # filter for elements that match the request arguments
        #i.e if q='amd ryzen', shows only amd ryzen elements
        # NOTE this filter stuff must be put into pymongo_interface
        
        return ll

class HelloWorld(Resource):
    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"
    def get(self):
        print(self.CONNECTION_STRING)
        return {'hello' : 'world'}

api.add_resource(SearchBar, '/api/search')
api.add_resource(HelloWorld, '/api/hello')