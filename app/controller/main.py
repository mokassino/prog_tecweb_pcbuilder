from flask import (
   Flask, 
   render_template,
   Blueprint
)

from app.controller.pymongo_interface import TableSearchInterface

#app = Flask(__name__)

bp = Blueprint('main',__name__)
api_bp = Blueprint('api', __name__)

@bp.route("/")
def index():
   CONNECTION_STRING = "mongodb+srv://pcbuilderdev:pcbuilderdev@pcbuilder-cluster.2hbnofk.mongodb.net/?retryWrites=true&w=majority"
   i = TableSearchInterface(CONNECTION_STRING)
   query = i.get_everything_buf()

   return render_template("index.html", data=query)

@bp.route("/pc-configuration")
def pc_configuration():
   return render_template("pc-configuration.html")

#if __name__ == '__main__':
#  app.run(debug = True)