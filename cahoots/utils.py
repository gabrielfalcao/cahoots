import json
import logging
import jwt
from flask import Response

logger = logging.getLogger(__name__)


def json_response(data, status=200, headers={}):
    serialized = json.dumps(data, indent=2, default=str)
    headers["Content-Type"] = "application/json"

    for key in headers.keys():
        value = headers.pop(key)
        headers[str(key)] = str(value)

    return Response(serialized, status=status, headers=headers)


def parse_jwt_token(token, verify=False, fallback=None, **kw):
    if not token:
        return fallback or {}
    else:
        logger.info(f"decoding JWT token")

    try:
        return jwt.decode(token, verify=verify, **kw)
    except Exception as e:
        logger.exception(f"failed to decode JWT while verifying signature: {e}")
        return parse_claims_cowboy_style(token)


def parse_claims_cowboy_style(token, fallback=None):
    # fallback in case jwt.decode fails (verify=True without a `secret`)
    logger.warning("trying to parse claims from token, cowboy style 🤡")
    try:
        parts = token.split(".")
        middle = parts[1]
        bjson = bytes(middle, "utf-8")
        raw = jwt.api_jws.base64url_decode(bjson)
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"could not parse JWT claims from {token!r} ({type(token)})")
        if fallback is None:
            fallback = {"claim_parse_error": str(e), "token": token}

        return fallback
