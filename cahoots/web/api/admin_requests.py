# -*- coding: utf-8 -*-
#
import logging
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import reqparse
from flask_restplus import inputs

from cahoots.models import AdminRequest
from .base import api, oidc

logger = logging.getLogger(__name__)


admin_request_json = api.model(
    "AdminRequest",
    {
        "method": fields.String(required=True),
        "path": fields.String(required=True),
        "args": fields.String(required=True),
        "data": fields.String(required=True),
        "headers": fields.String(required=True),
        "jwt_token": fields.String(required=True),
    },
)

parser = reqparse.RequestParser()
# parser.add_argument('oidc_id_token', location='cookies', help='the id token provided by keycloak')
# parser.add_argument('session', location='cookies', help='the session id containing the state of authentication')

admin_request_ns = api.namespace(
    "AdminRequest API V1", description="Fake NewStore AdminRequest API", path="/api/v1"
)


@admin_request_ns.route("/admin-requests")
@admin_request_ns.expect(parser)
class AdminRequestListEndpoint(Resource):
    def get(self):
        admin_requests = AdminRequest.all()
        return [u.to_dict() for u in admin_requests]

    def delete(self):
        response = []
        try:
            for admin_request in AdminRequest.all():
                admin_request.delete()
                response.append(admin_request.to_dict())
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 400


@admin_request_ns.route("/admin_request/<admin_request_id>")
class AdminRequestEndpoint(Resource):
    def get(self, admin_request_id):
        admin_request = AdminRequest.find_one_by(id=admin_request_id)
        if not admin_request:
            return {"error": "admin_request not found"}, 404

        return admin_request.to_dict()

    def delete(self, admin_request_id):
        admin_request = AdminRequest.find_one_by(id=admin_request_id)
        if not admin_request:
            return {"error": "admin_request not found"}, 404

        admin_request.delete()
        return {"deleted": admin_request.to_dict()}
