import json
import logging
from typing import Optional
from uiclasses import Model as DataClass
from chemist import Model, db, metadata
from cahoots.utils import parse_jwt_token


logger = logging.getLogger(__name__)


class Template(Model):
    table = db.Table(
        "templates",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("name", db.UnicodeText, nullable=True, index=True),
        db.Column("content", db.UnicodeText, nullable=True),
    )

    @property
    def content(self):
        try:
            return json.loads(self.get("content", "null"), default=str)
        except Exception:
            logger.exception(f"{self}.content property")
            return self.get("content")


class OpaqueJWT(DataClass):
    opaque: str

    def initialize(self, **kw):
        self.__jwt__ = None

    @property
    def jwt(self) -> Optional[dict]:
        if not self.__jwt__:
            self.__jwt__ = parse_jwt_token(self.opaque, fallback={})

        return self.__jwt__

    @property
    def sub(self):
        return self.jwt.get('sub')

    @property
    def iss(self):
        return self.jwt.get('iss')

    @property
    def type(self):
        return self.jwt.get('typ') or 'unknown'

    @property
    def scope(self):
        return self.jwt.get('scope')


class JWTToken(Model):
    table = db.Table(
        "jwt_tokens",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("type", db.Unicode(100), nullable=True, index=True),
        db.Column("opaque_data", db.UnicodeText, nullable=True),
    )

    @classmethod
    def get_or_create_from_opaque_data(cls, data: str):
        jwt = OpaqueJWT(opaque=data)
        return cls.get_or_create_from_opaque_jwt(jwt)

    @classmethod
    def get_or_create_from_opaque_jwt(cls, jwt: OpaqueJWT):
        return cls.get_or_create(opaque_data=jwt.opaque, type=jwt.type)


class AdminRequest(Model):
    table = db.Table(
        "keycloak_admin_requests",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("method", db.Unicode(20), nullable=True, index=True),
        db.Column("path", db.UnicodeText, nullable=True, index=True),
        db.Column("jwt_token", db.UnicodeText, nullable=True),
        db.Column("args", db.UnicodeText, nullable=True),
        db.Column("data", db.UnicodeText, nullable=True),
        db.Column("headers", db.UnicodeText, nullable=True),
    )

    @property
    def args(self):
        return json.loads(self.get("args", "{}"))

    @property
    def jwt_token(self):
        return json.loads(self.get("jwt_token", "{}"))

    @property
    def data(self):
        return json.loads(self.get("data", "{}"))

    @property
    def headers(self):
        return json.loads(self.get("headers", "{}"))

    # def to_dict(self):
    #     data = self.serialize()
    #     data["headers"] = self.headers
    #     data["data"] = self.data
    #     data["args"] = self.args
    #     data["jwt_token"] = self.jwt_token
    #     return data
