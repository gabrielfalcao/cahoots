import os
import redis
from pathlib import Path

module_path = Path(__file__).parent

current_working_path = Path(os.getcwd()).expanduser().absolute()

DEFAULT_UPLOAD_PATH = current_working_path.joinpath("cahoots-in-uploads")
APP_URL_EXTERNAL = os.getenv("APP_URL_EXTERNAL") or "https://pron-f1l3-serv3r.ngrok.io/"

REDIS_HOST = os.getenv("REDIS_HOST")
if REDIS_HOST:
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.Redis(
        host=REDIS_HOST or "localhost", port=int(os.getenv("REDIS_PORT") or 6379), db=0
    )
else:
    SESSION_TYPE = "filesystem"

# set this to true when serving the application via HTTPS or else the
# flask-restful routes won't show up on swagger.
HTTPS_API = os.getenv("HTTPS_API")

SECRET_KEY = b"//>;,;42zy_{lz@eat-m00r3-AsS)f:P128<\\"
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") or str(DEFAULT_UPLOAD_PATH)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


OAUTH2_DOMAIN = os.getenv("OAUTH2_DOMAIN") or "id.t.newstore.net"
OAUTH2_CALLBACK_URL = (
    os.getenv("OAUTH2_CALLBACK_URL")
    or "https://cahoots.in/callback/oauth2"
)

# https://id.t.newstore.net/admin/master/console/#/realms/gabriel-NA-43928/clients/c75308f7-99e9-4b18-aeca-6e742a0b361d/credentials
OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
OAUTH2_BASE_URL = (
    os.getenv("OAUTH2_BASE_URL")
    or "https://id.t.newstore.net/realms/gabriel-NA-43928/protocol/openid-connect/"
)
OAUTH2_ACCESS_TOKEN_URL = (
    os.getenv("OAUTH2_ACCESS_TOKEN_URL") or f"{OAUTH2_BASE_URL}/token"
)
OAUTH2_AUTHORIZE_URL = os.getenv("OAUTH2_AUTHORIZE_URL") or "{OAUTH2_BASE_URL}/auth"
OAUTH2_CLIENT_SCOPE = (
    os.getenv("OAUTH2_CLIENT_SCOPE")
    or "openid profile email roles role_list profile picture email_verified http://newstore/flask-test http://newstore/newstore_id"
)
OAUTH2_CLIENT_AUDIENCE = (
    os.getenv("OAUTH2_CLIENT_AUDIENCE") or "https://cahoots.in/"
)
DOCKER_IMAGE = (
    os.getenv("DOCKER_IMAGE") or "latest"
)

OIDC_CLIENT_SECRETS = os.getenv("OIDC_CLIENT_SECRETS_JSON_PATH") or str(
    module_path.joinpath("client_secrets.json")
)
OIDC_ID_TOKEN_COOKIE_SECURE = bool(os.getenv("OIDC_ID_TOKEN_COOKIE_SECURE"))
OIDC_REQUIRE_VERIFIED_EMAIL = bool(os.getenv("OIDC_REQUIRE_VERIFIED_EMAIL"))
# OIDC_VALID_ISSUERS = None
OIDC_OPENID_REALM = os.getenv("OIDC_OPENID_REALM")
# OIDC_CALLBACK_ROUTE = '/callback_oidc'
OIDC_SCOPES = [
    "openid",
    "email",
    "profile",
    "roles",
    "address",
    "microprofile-jwt",
    "phone",
    "offline_access",
]
# OIDC_USER_INFO_ENABLED = True


class dbconfig:
    host = os.getenv("POSTGRES_HOST") or "localhost"
    port = int(os.getenv("POSTGRES_PORT") or 5432)
    username = os.getenv("POSTGRES_USERNAME") or "cahoots_in"
    password = os.getenv("POSTGRES_PASSWORD") or "Wh15k3y"
    database = os.getenv("POSTGRES_DATABASE") or "cahoots_in"
    auth = os.getenv("POSTGRES_AUTH") or (
        password and f"{username}:{password}" or username
    )
    domain = os.getenv("POSTGRES_DOMAIN") or f"{host}:{port}"

    @classmethod
    def sqlalchemy_url(config):
        return "/".join(
            [
                f"postgresql+psycopg2:/",
                f"{config.auth}@{config.domain}",
                f"{config.database}",
            ]
        )
