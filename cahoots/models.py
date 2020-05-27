import json
import logging

from datetime import datetime
from chemist import Model, db, metadata, DefaultForeignKey


logger = logging.getLogger(__name__)


def ensure_datetime(value):
    if isinstance(value, str):
        try:
            value = int(value)
        except (TypeError, ValueError):
            logger.warning(
                f"cannot convert timestamp to datetime: {value!r}. "
                "Datetime will be NULL."
            )
            return None

    if isinstance(value, (float, int)):
        return datetime.fromtimestamp(value)

    elif isinstance(value, datetime):
        return value

    return value


class User(Model):
    table = db.Table(
        "user",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("oidc_sub", db.UnicodeText, nullable=True, index=True),
        db.Column("email", db.String(100), nullable=False, unique=True),
        db.Column("first_name", db.String(255)),
        db.Column("last_name", db.String(255)),
        db.Column("profile_picture", db.UnicodeText),
        db.Column("created_at", db.DateTime, default=datetime.utcnow),
        db.Column("updated_at", db.DateTime, default=datetime.utcnow),
        db.Column("extra_data", db.UnicodeText),
    )

    def to_dict(self):
        data = self.serialize()
        data.pop("extra_data", None)
        data.update(self.extra_data)
        return data

    @property
    def extra_data(self):
        value = self.get("extra_data")
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            logger.warning(f"{self}.extra_data is not a valid JSON")
            return {"value": value, "error": str(e)}

    def save(self, *args, **kw):
        self.set(updated_at=datetime.utcnow())
        return super().save(*args, **kw)

    def add_token(
        self,
        id_token: str,
        access_token: str,
        expires_in: int = None,
        expires_at: datetime = None,
        scope: str = None,
        token_type: str = None,
        **extra_data,
    ):
        token = UserToken.get_or_create(user_id=self.id, id_token=json.dumps(id_token))
        token.update_and_save(
            access_token=access_token,
            expires_at=ensure_datetime(expires_at),
            expires_in=expires_in,
            scope=scope,
            token_type=token_type,
            extra_data=json.dumps(extra_data, indent=4, default=str),
        )
        return token


class UserToken(Model):
    table = db.Table(
        "user_tokens",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("id_token", db.UnicodeText, nullable=True),
        db.Column("access_token", db.UnicodeText, nullable=True, index=True),
        db.Column("expires_at", db.DateTime),
        db.Column("expires_in", db.Integer),
        db.Column("scope", db.Text),
        db.Column("token_type", db.Text),
        db.Column("extra_data", db.UnicodeText),
        DefaultForeignKey("user_id", "user.id"),
    )

    @property
    def user(self):
        return User.find_one_by(id=self.user_id)

    @property
    def scope(self):
        return self.get("scope", "").split()

    @property
    def extra_data(self):
        value = self.get("extra_data")
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            logger.warning(f"{self}.extra_data is not a valid JSON")
            return {"value": value, "error": str(e)}

    def to_dict(self):
        data = self.serialize()
        data.pop("extra_data", None)
        data.pop("scope", None)
        data.update(self.extra_data)
        data["scope"] = self.scope
        return data


class JWTToken(Model):
    table = db.Table(
        "user_jwt_tokens",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("data", db.UnicodeText, nullable=True, index=True),
        DefaultForeignKey("user_id", "user.id"),
    )

    @property
    def user(self):
        return User.find_one_by(id=self.user_id)

    @property
    def data(self):
        return json.loads(self.get("data", "null"))

    def to_dict(self):
        data = self.serialize()
        data["data"] = self.data
        return data


class Resume(Model):
    table = db.Table(
        "user_resumes",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("title", db.UnicodeText, nullable=True, index=True),
        db.Column("work_experience", db.UnicodeText, nullable=True, index=True),
        db.Column("academic_background", db.UnicodeText, nullable=True, index=True),
        db.Column("extra_sections", db.UnicodeText, nullable=True, index=True),
        DefaultForeignKey("user_id", "user.id"),
    )

    @property
    def user(self):
        return User.find_one_by(id=self.user_id)

    @property
    def work_experience(self):
        return json.loads(self.get("work_experience", "null"))

    @property
    def academic_background(self):
        return json.loads(self.get("academic_background", "null"))

    @property
    def extra_sections(self):
        return json.loads(self.get("extra_sections", "null"))

    def to_dict(self):
        data = self.serialize()
        data["work_experience"] = self.work_experience
        data["academic_background"] = self.academic_background
        data["extra_sections"] = self.extra_sections
        return data


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
            logger.exception(f'{self}.content property')
            return self.get("content")


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
