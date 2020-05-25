# -*- coding: utf-8 -*-
import json
import logging
import jwt

from flask import redirect, session, request, g, url_for

from cahoots.utils import json_response
from cahoots.web import db
from cahoots.web.core import application
from cahoots.web.core import oidc


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


@application.before_request
def set_global_vars():
    user_id = session.get('user_id')
    if not user_id:
        return
    g.user = db.User.find_one_by(id=user_id)
    g.access_token = parse_jwt_token(session.get('access_token'))
    g.refresh_token = parse_jwt_token(session.get('refresh_token'))


def parse_jwt_token(token):
    if not token:
        return {}
    try:
        return jwt.decode(token)
    except Exception as e:
        logger.warning(f'failed to decode JWT while verifying signature: {e}')
        try:
            raw = jwt.api_jws.base64url_decode(token.split('.')[1])
            return json.loads(raw)
        except Exception as e:
            logger.exception(f'could not parse token {token!r}')
            return {'error': str(e), 'token': token}


@application.route("/login/oauth2")
@oidc.require_login
def login_oauth2():
    id_token = oidc.get_cookie_id_token()
    access_token = oidc.get_access_token()
    refresh_token = oidc.get_refresh_token()

    user, token = db.get_user_and_token_from_userinfo(id_token, parse_jwt_token(access_token))
    session['id_token'] = id_token
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['user_id'] = user.id
    set_global_vars()
    return redirect('/')


@application.route("/auth/admin", methods=["GET", "POST"])
def auth_admin_push_revokation():
    logger.info(f"Keycloak sent headers: {request.headers}")
    logger.info(f"Keycloak sent args: {request.args}")
    logger.info(f"Keycloak sent data {request.data}")
    return json_response({
        'args': request.args,
        'data': request.data,
        'headers': dict(request.headers),
    })


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
    oidc.logout()
    session.clear()
    return redirect(request.args.get('next') or url_for("index"))
