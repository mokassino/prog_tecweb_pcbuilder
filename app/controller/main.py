from flask import (
   Flask, 
   render_template,
   Blueprint
)
#app = Flask(__name__)

bp = Blueprint('main',__name__)

@bp.route("/")
def index():
   return render_template("index.html")

@bp.route("/pc-configuration")
def pc_configuration():
   return render_template("pc-configuration.html")

#if __name__ == '__main__':
#  app.run(debug = True)