# -*- coding: utf-8 -*-
import json
import logging

from flask import redirect, session, request, g, url_for, make_response
from cahoots.models import AdminRequest, JWTToken, OpaqueJWT
from cahoots.utils import json_response, parse_jwt_token

from cahoots.web.core import application
from cahoots.web.core import oidc


logger = logging.getLogger(__name__)

AUTH_SESSION_KEYS = {"access_token", "refresh_token"}


@application.context_processor
def inject_functions():
    return dict(is_authenticated=is_authenticated())


@application.context_processor
def inject_user_when_present():
    if not is_authenticated():
        return {"user": None}

    user = getattr(g, "user", None)
    return dict(user=user)


@application.before_request
def set_global_vars(tokens: dict = None):
    tokens = tokens or session

    # id_token is the only dict, access_token and refresh_token are an
    # opaque JWT
    g.id_token = tokens.get('id_token') or {}
    for key in AUTH_SESSION_KEYS:
        opaque = tokens.get(key)
        if not opaque:
            continue

        jwt = OpaqueJWT(opaque=opaque)
        model = JWTToken.get_or_create_from_opaque_jwt(jwt)
        setattr(g, key, jwt.jwt)


@application.route("/login/oauth2")
@oidc.require_login
def login_oauth2():
    id_token = oidc.get_cookie_id_token()
    access_token = oidc.get_access_token()
    refresh_token = oidc.get_refresh_token()
    tokens = locals()

    session.update(tokens)
    set_global_vars(tokens)
    return redirect("/")


@application.route("/auth/admin", methods=["GET", "POST"])
@application.route("/auth/admin/<path:path>", methods=["GET", "POST"])
def auth_admin_push_revokation(path=""):
    logger.info(f"Keycloak sent {request.method}: {request.path}")
    logger.info(f"Keycloak sent {json.dumps(request.headers, indent=4, default=str)}")
    logger.info(f"Keycloak sent args: {request.args!r}")
    logger.info(f"Keycloak sent data {request.data!r}")
    jwt_token = parse_jwt_token(request.data)
    record = AdminRequest.create(
        **{
            "path": request.path,
            "method": request.method,
            "args": json.dumps(request.args, default=str),
            "data": json.dumps(request.data, default=str),
            "jwt_token": json.dumps(jwt_token, default=str),
            "headers": json.dumps(request.headers, default=str),
        }
    )
    return json_response(record.to_dict())


def is_authenticated():
    return AUTH_SESSION_KEYS.intersection(set(session.keys()))


@application.route("/logout")
def logout():
    response = make_response(redirect(request.args.get("next") or url_for("index")))
    response.delete_cookie("session")
    response.delete_cookie("oidc_id_token")
    oidc.logout()
    session.clear()
    return response
