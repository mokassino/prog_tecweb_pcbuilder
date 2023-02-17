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
import json
import sqlite3
import os
from controller.pymongo_interface import SearchBarInterface, FilterTableSearchInterface
import controller.db
from controller.user import User
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
app.secret_key = "secrete"

CONNECTION_STRING = "mongodb+srv://pcbuilderdev:pcbuilderdev@pcbuilder-cluster.2hbnofk.mongodb.net/?retryWrites=true&w=majority"

# Naive database setup
try:
    controller.db.init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

@app.route("/")
def index():
   i = FilterTableSearchInterface(CONNECTION_STRING)
   d = request.args
   query = i.filter(request.args)
   if current_user.is_authenticated:
      j = True
   else:
      j = False

   return render_template("index.html", data=query, is_authenticated=j)

@app.route("/pc-configuration")
def pc_configuration():
   return render_template("pc-configuration.html")


class SearchBar(Resource):
    def get(self):
      args = request.args

      if 'q' in args.keys():
         q = args['q'] # prob should parse with marshmallow?
      else:
         q = None

      l = SearchBarInterface(CONNECTION_STRING).get_everything(q)
      return l

@login_manager.user_loader
def load_user(user_id):
   # https://flask-login.readthedocs.org/en/latest/#how-it-works
    return User.get(user_id)

api.add_resource(SearchBar, '/api/search')
Talisman(app, content_security_policy=False)

# Login
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

# Login Callback
@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    print(code)

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    result = token_response.text
    print(result)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in

    unique_id = userinfo_response.json()["sub"]    
    t = login_user(user)
    print(t)

    # Send user back to homepage
    return redirect(url_for("index"))

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context="adhoc")