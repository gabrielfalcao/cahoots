# -*- coding: utf-8 -*-
#
import logging
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import reqparse
from flask_restplus import inputs

from cahoots.models import Template
from .base import api, oidc

logger = logging.getLogger(__name__)


template_json = api.model(
    "Template",
    {
        "name": fields.String(
            required=True, description="name unique name for this template"
        ),
        "content": fields.String(
            required=True, description="the JSON data representing the template"
        ),
    },
)

parser = reqparse.RequestParser()
parser.add_argument("access_token", location="args", help="The opaque JWT Acess Token")

# parser.add_argument('oidc_id_token', location='cookies', help='the id token provided by keycloak')
# parser.add_argument('session', location='cookies', help='the session id containing the state of authentication')

template_ns = api.namespace(
    "Template API V1",
    description="Fake NewStore Template API",
    path="/api/v1/templates",
)


@template_ns.route("/templates")
@template_ns.expect(parser)
class TemplateListEndpoint(Resource):
    @oidc.accept_token(True, scopes_required=["template:read"])
    def get(self):
        templates = Template.all()
        return [u.to_dict() for u in templates]

    @template_ns.expect(template_json)
    @oidc.accept_token(True, scopes_required=["template:write"])
    def post(self):
        name = api.payload.get("name")
        content = api.payload.get("content")
        try:
            template = Template.create(name=name, content=content)
            return template.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @oidc.accept_token(True, scopes_required=["template:write"])
    def delete(self):
        response = []
        try:
            for template in Template.all():
                template.delete()
                response.append(template.to_dict())
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 400


@template_ns.route("/template/<template_id>")
@template_ns.expect(parser)
class TemplateEndpoint(Resource):
    @oidc.accept_token(True, scopes_required=["template:read"])
    def get(self, template_id):
        template = Template.find_one_by(id=template_id)
        if not template:
            return {"error": "template not found"}, 404

        return template.to_dict()

    @oidc.accept_token(True, scopes_required=["template:write"])
    def delete(self, template_id):
        template = Template.find_one_by(id=template_id)
        if not template:
            return {"error": "template not found"}, 404

        template.delete()
        return {"deleted": template.to_dict()}

    @oidc.accept_token(True, scopes_required=["template:write"])
    @template_ns.expect(template_json)
    def put(self, template_id):
        template = Template.find_one_by(id=template_id)
        if not template:
            return {"error": "template not found"}, 404

        name = api.payload.get("name")
        content = api.payload.get("content")
        template = template.update_and_save(name=name, content=content)
        return template.to_dict(), 200
