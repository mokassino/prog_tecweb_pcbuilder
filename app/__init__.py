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

        CONNECTION_STRING = "mongodb+srv://pcbuilderdev:pcbuilderdev@pcbuilder-cluster.2hbnofk.mongodb.net/?retryWrites=true&w=majority"
        l = pymongo_interface.SearchBarInterface(CONNECTION_STRING).get_everything(q)
        
        return l

api.add_resource(SearchBar, '/api/search')