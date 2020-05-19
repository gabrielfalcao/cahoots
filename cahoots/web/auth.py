# -*- coding: utf-8 -*-
# import json
import logging

from flask import redirect, session, request, g, url_for

# from cahoots.models import JWTToken
from . import db
from .core import application
from .core import oidc

logger = logging.getLogger(__name__)


@application.context_processor
def inject_functions():
    return dict(is_authenticated=is_authenticated())


@application.context_processor
def inject_user_when_present():
    if not is_authenticated():
        return {"user": None}

    user = getattr(g, "user", None)
    return dict(user=user)


@application.route("/login/oauth2")
@oidc.require_login
def login_oauth2():
    id_token = oidc.get_cookie_id_token()
    access_token = oidc.get_access_token() or {}
    user = db.get_user_and_token_from_userinfo(id_token, access_token)
    session['id_token'] = id_token
    session['access_token'] = access_token
    session['user'] = user.to_dict()
    return redirect('/api/')


# @application.route("/callback/oauth2")
# def oauth2_callback():

#     # Handles response from token endpoint
#     try:
#         token = oauth2.authorize_access_token()
#     except Exception as e:
#         return render_template(
#             "error.html",
#             exception="Failed to retrieve OAuth2 userinfo",
#             message=str(e),
#             args=dict(request.args),
#         )

#     response = oauth2.get("userinfo")

#     userinfo = response.json()

#     encoded_jwt_token = token.get("access_token")
#     encoded_id_token = token.get("id_token")
#     jwt_token = jwt.decode(encoded_jwt_token, verify=False)
#     id_token = jwt.decode(encoded_id_token, verify=False)

#     session["oidc_sub"] = userinfo.get("sub")
#     userinfo["jwt_token"] = jwt_token
#     session["token"] = token
#     session["access_token"] = encoded_jwt_token
#     session["id_token"] = id_token
#     session["jwt_token"] = jwt_token

#     user, token = db.get_user_and_token_from_userinfo(
#         token=token,
#         userinfo=userinfo,
#     )
#     session["user"] = user.to_dict()
#     session["token"] = token.to_dict()

#     return redirect("/dashboard")


def is_authenticated():
    auth_keys = {"user", "access_token", "token", "id_token", "jwt_token"}
    return auth_keys.intersection(set(session.keys()))


@application.route("/logout")
def logout():
    # Clear session stored data
    session.clear()
    return redirect(request.args.get('next') or url_for("index"))
