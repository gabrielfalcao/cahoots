# -*- coding: utf-8 -*-

from flask import render_template

from cahoots.logs import set_log_level_by_name
from cahoots.web.core import application
from cahoots import config


logger = set_log_level_by_name("DEBUG", __name__)


@application.route("/", methods=["GET"])
def index():
    return render_template("token-debug.html")
