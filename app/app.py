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
from controller.pymongo_interface import SearchBarInterface, FilterTableSearchInterface, SaveBuildInterface
from controller.user import User
from flask_restful import Resource,Api, request
from oauthlib.oauth2 import WebApplicationClient
from flask_talisman import Talisman
from hashlib import sha256
import yaml


config = yaml.safe_load(open("config.yml"))
GOOGLE_CLIENT_ID = config["google"]["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["google"]["GOOGLE_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = config["google"]["GOOGLE_DISCOVERY_URL"] 
CONNECTION_STRING = config["mongodb"]

app = Flask(__name__, instance_relative_config=True)
    
login_manager = LoginManager()
login_manager.init_app(app)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

bp = Blueprint('main',__name__)
api_bp = Blueprint('api', __name__)

api = Api(api_bp)
app.register_blueprint(bp)
app.register_blueprint(api_bp)
app.secret_key = config["secret"]

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

@app.route("/saved-builds")
@login_required
def pc_configuration():
    sbi = SaveBuildInterface(CONNECTION_STRING)
    email = current_user.email

    l = sbi.get_every_build_ref(email)

    return render_template("pc-configuration.html", data=l)

@app.route("/saved-builds/<build_id>")
def saved_build_id(build_id): # render template with data for that build
    sbi = SaveBuildInterface(CONNECTION_STRING)

    # Get build by url with every date
    try:
        email = current_user.email
    except AttributeError as e: #Request wasn't made by a logged user
        email = None

    db = sbi.get_sb()
    query = {"url" : build_id}
    filter = {"_id" : 0, "email" : 0, "url" : 0}

    # Pack every name into a list
    build = list(db.find(query, filter))
    t = build[0]
    t.pop("name")

    # For every value in the dictionary, create another dictionary 
    # with additional info for each part like price, amazon link
    db = sbi.get_db()
    traduction = dict({"Scheda Madre" : "motherboard", "CPU" : "cpu", "GPU" : "gpu", "RAM" : "ram" , "SSD" : "ssd", "Alimentatore" : "alim"})

    data = list()

    for key in t.keys(): # for each part in the selected build
        part = db[traduction[key]].find({"_id" : t[key]})
        try:
            part = part[0]
            data.append({"part" : [key, part['_id'], part['price'], part['url']]})
        except IndexError as e:
            data.append({"part" : [key, '', '', '']})

    if email == None:
        return render_template("saved-build-id.html", data=data, url=build_id, logged=False)
    else:
        return render_template("saved-build-id.html", data=data, url=build_id, logged=True)

@app.route("/delete-build")
@login_required
def delete_saved_build():
    args = request.args
    if 'q' in args.keys(): # q=ALPHANUMERIC_URL 
        sbi = SaveBuildInterface(CONNECTION_STRING)
        sbi.delete_build(current_user.email, args['q'] ) # Delete the selected build
        sbi.close() 

    return redirect("/saved-builds")

class SearchBar(Resource): # Implement RESTful for items in the DB
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
Talisman(app, content_security_policy=False) # Implements HTTPS and Security HEADERS in requests

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

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
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

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    result = token_response.text

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
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/save-build")
@login_required
def save_build():
    # when an user click on "Salva build", the front-end sends to
    # the back-end the items names contained in the choosen items table
    # then this function contact the db and save these items and the email 
    # associated to the user
    email = current_user.email
    args = request.args
    keys = args.keys()
    doc = {"email" : email}
    for k in keys:
        doc =  {**doc, **{k : args[k]} }

    sbi = SaveBuildInterface(CONNECTION_STRING)
    sbi.save_build(doc)

    return redirect(url_for("index"))

#if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)

