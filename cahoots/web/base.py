# -*- coding: utf-8 -*-

from flask import render_template

from cahoots.logs import set_log_level_by_name
from cahoots.web.core import application
# from cahoots import config


logger = set_log_level_by_name("DEBUG", __name__)


@application.route("/backend")
def backend():
    return render_template("token-debug.html")


@application.route("/")
@application.route("/admin")
@application.route("/app")
@application.route("/app/<path:path>")
@application.route("/login")
@application.route("/oauth2/callback")
def index(path=None):
    return render_template("index.html")
