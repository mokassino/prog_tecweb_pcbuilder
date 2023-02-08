from flask import Flask, Blueprint
from flask_restful import Resource,Api
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
        processors = pymongo_interface.PymongoInterface(CONNECTION_STRING).get_processors()

        l = list(processors.find())
        
        return l

class HelloWorld(Resource):
    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"
    def get(self):
        print(self.CONNECTION_STRING)
        return {'hello' : 'world'}

api.add_resource(SearchBar, '/api/search')
api.add_resource(HelloWorld, '/api/hello')