from flask import (
   Flask, 
   render_template,
   Blueprint,
   request,
   redirect,
   url_for
)

from flask_login import (
   LoginManager,
   current_user,
   login_required,
   login_user,
   logout_user,
)

import requests
from controller.pymongo_interface import SearchBarInterface, FilterTableSearchInterface
from flask_restful import Resource,Api, request
from oauthlib.oauth2 import WebApplicationClient
from flask_talisman import Talisman


GOOGLE_CLIENT_ID = "499806511986-9666ki8p6vjo8udjecn71qrt5c5oe9p1.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

app = Flask(__name__, instance_relative_config=True)
    
login_manager = LoginManager()
login_manager.init_app(app)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

bp = Blueprint('main',__name__)
api_bp = Blueprint('api', __name__)

api = Api(api_bp)
app.register_blueprint(bp)
app.register_blueprint(api_bp)


@app.route("/")
def index():
   CONNECTION_STRING = "mongodb+srv://pcbuilderdev:pcbuilderdev@pcbuilder-cluster.2hbnofk.mongodb.net/?retryWrites=true&w=majority"
   i = FilterTableSearchInterface(CONNECTION_STRING)
   d = request.args
   query = i.filter(request.args)

   return render_template("index.html", data=query)

@app.route("/pc-configuration")
def pc_configuration():
   return render_template("pc-configuration.html")


class SearchBar(Resource):
    def get(self):
      args = request.args
      CONNECTION_STRING = "mongodb+srv://pcbuilderdev:pcbuilderdev@pcbuilder-cluster.2hbnofk.mongodb.net/?retryWrites=true&w=majority"

      if 'q' in args.keys():
         q = args['q'] # prob should parse with marshmallow?
      else:
         q = None

      l = SearchBarInterface(CONNECTION_STRING).get_everything(q)
      return l

@login_manager.user_loader
def load_user(user_id):
    # https://flask-login.readthedocs.org/en/latest/#how-it-works

    user = user.User();
    return user.get_id()

api.add_resource(SearchBar, '/api/search')
Talisman(app, content_security_policy=False)

#if __name__ == '__main__':
#  app.run(debug = True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context="adhoc")