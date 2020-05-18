from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_session import Session
from flask_oidc import OpenIDConnect

from cahoots.filesystem import templates_path, static_path

params = {
    "template_folder": str(templates_path),
    "static_url_path": "/static/",
    "static_folder": str(static_path),
}

application = Flask(__name__, **params)
application.config.from_object("cahoots.config")

cors = CORS(application, resources="*")

session_manager = Session(application)
oidc = OpenIDConnect(application)
