# -*- coding: utf-8 -*-
#

import os
from pathlib import Path
from flask import request, redirect, url_for, send_from_directory
from flask import render_template, jsonify
from typing import Optional
from werkzeug.utils import secure_filename

from cahoots.logs import set_log_level_by_name
from cahoots.web.core import application
from cahoots import config
from cahoots.web import backend

logger = set_log_level_by_name("DEBUG", __name__)

upload_path = Path(config.UPLOAD_FOLDER)


@application.route("/", methods=["GET"])
def index():
    return render_template("token-debug.html")


@application.route("/", methods=["GET"])
def dashboard():
    return render_template("token-debug.html")


def get_upload_path_to_filename(filename):
    filename = secure_filename(filename)
    if not upload_path.exists():
        upload_path.mkdir(parents=True)
    elif not upload_path.is_dir():
        raise RuntimeError(
            f"Invalid upload path: {upload_path!r} - Exists and is not a directory."
        )

    destination = os.path.join(application.config["UPLOAD_FOLDER"], filename)
    return destination


@application.route("/upload", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    if "file" not in request.files:
        logger.warning(f"no file in request {request}")
        return redirect(request.url)

    candidates = request.files.getlist("file")
    files = list(filter(bool, [handle_file_upload(file) for file in candidates]))

    if not files:
        logger.error(f"{len(files)} of {len(candidates)} were uploaded")

    return jsonify(backend.list_files().to_dict())


def handle_file_upload(file) -> Optional[Path]:
    if not file:
        logger.error(f"{file!r} is not a file")
        return
    # if user does not select file, browser also
    # submit a empty part without filename
    if not file.filename:
        logger.error(f"no filename {file}")
        return

    if file:
        filename = get_upload_path_to_filename(file.filename)
        file.save(filename)
        return Path(filename)


@application.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(application.config["UPLOAD_FOLDER"], filename)


@application.route("/files")
def list_files():
    files = backend.list_files()
    return jsonify(files.to_dict())
