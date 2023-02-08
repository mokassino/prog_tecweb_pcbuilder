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
        args = request.args
        q = args['q'] # bad security practice here, everything could go in args, it's better to parse with marshmallow

        CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"
        l = pymongo_interface.SearchBarInterface(CONNECTION_STRING).get_processors(q)
        
        return l

class HelloWorld(Resource):
    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"
    def get(self):
        print(self.CONNECTION_STRING)
        return {'hello' : 'world'}

api.add_resource(SearchBar, '/api/search')
api.add_resource(HelloWorld, '/api/hello')