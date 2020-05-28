# -*- coding: utf-8 -*-

from flask import render_template

from cahoots.logs import set_log_level_by_name
from cahoots.web.core import application
# from cahoots import config


logger = set_log_level_by_name("DEBUG", __name__)


@application.route("/backend", methods=["GET"])
def backend():
    return render_template("token-debug.html")


@application.route("/", methods=["GET"])
@application.route("/app", methods=["GET"])
@application.route("/app/<path:path>", methods=["GET"])
def index(path=None):
    return render_template("index.html")
