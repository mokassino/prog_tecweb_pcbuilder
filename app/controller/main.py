from flask import (
   Flask, 
   render_template,
   Blueprint
)

from app.controller.pymongo_interface import SearchBarInterface

#app = Flask(__name__)

bp = Blueprint('main',__name__)
api_bp = Blueprint('api', __name__)

@bp.route("/")
def index():
   i = SearchBarInterface("mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority")
   query = i.get_everything()

   return render_template("index.html", data=query)

@bp.route("/pc-configuration")
def pc_configuration():
   return render_template("pc-configuration.html")

#if __name__ == '__main__':
#  app.run(debug = True)