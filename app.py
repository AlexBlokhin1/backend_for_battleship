from flask import Flask, render_template
import responder
from flask_cors import CORS

from methods_for_battleship import find_players
from logging import getLogger
_logger = getLogger(__name__)

ALLOWED_HOSTS = {r"/":          {"origins": "*"},
                 r"/pre_game":  {"origins": "*"}}


# EXAMPLE OF APP ROUTE @app.route('/result', methods=['post', 'get'])


app = Flask(__name__, static_folder='static/')

cors = CORS(app, resources=ALLOWED_HOSTS)
############# todo    what this? -- ! -- (see line just below)
api = responder.API(allowed_hosts=["'http://192.168.0.100:8080",
                                   "http://localhost:8080",
                                   "http://192.168.0.101:8080",
                                   "http://192.168.0.101:8080",
                                   "http://192.168.0.102:8080",
                                   "http://localhost:8081/ ",
                                   "http://192.168.0.102:8081/"])

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['post', 'get'])
def home():
    return find_players()


@app.route("/index", methods=['post', 'get'])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
