# -*- coding: utf-8 -*-
#
import logging
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import fields
from flask import url_for, jsonify
from .base import application

from cahoots import config
from cahoots.models import Resume
from cahoots.worker.client import EchoClient

from cahoots.web.core import oidc
logger = logging.getLogger(__name__)


if config.HTTPS_API:

    # monkey-patch Flask-RESTful to generate proper swagger url
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint("specs"), _external=True, _scheme="https")

    logger.warning(
        "monkey-patching swagger to support https " "(because HTTPS_API env var is set)"
    )
    Api.specs_url = specs_url


api = Api(application, doc="/api/")

resume_json = api.model(
    "Resume",
    {
        "id": fields.String(required=False, description="the resume id"),
        "title": fields.String(required=False, description="title"),
        "work_experience": fields.String(required=False, description="work_experience"),
        "academic_background": fields.String(required=False, description="academic_background"),
    },
)

ns = api.namespace("Resume API V1", description="CRUD API for Resumes attached to a user", path="/api/v1/")


@ns.route("/resume")
class ResumeListEndpoint(Resource):
    # @oidc.accept_token(True, scopes_required=['resume:list', 'resume:admin'])
    def get(self):
        resumes = Resume.all()
        return [u.to_dict() for u in resumes]

    @ns.expect(resume_json)
    @oidc.accept_token(True, scopes_required=['resume:create', 'resume:write', 'resume:admin'])
    def post(self):
        title = api.payload.get("title")
        academic_background = api.payload.get("academic_background")
        work_experience = api.payload.get("work_experience")
        try:
            resume = Resume.create(
                title=title,
                academic_background=academic_background,
                work_experience=work_experience,
            )
            return resume.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @oidc.accept_token(True, scopes_required=['resume:admin'])
    def delete(self):
        response = []
        try:
            for resume in Resume.all():
                resume.delete()
                response.append(resume.to_dict())
            return response, 200
        except Exception as e:
            return {"error": str(e)}, 400


@ns.route("/resume/<resume_id>")
class ResumeEndpoint(Resource):
    @oidc.accept_token(True, scopes_required=['resume:read', 'resume:admin'])
    def get(self, resume_id):
        resume = Resume.find_one_by(id=resume_id)
        if not resume:
            return {"error": "resume not found"}, 404

        return resume.to_dict()

    @oidc.accept_token(True, scopes_required=['resume:delete', 'resume:admin'])
    def delete(self, resume_id):
        resume = Resume.find_one_by(id=resume_id)
        if not resume:
            return {"error": "resume not found"}, 404

        resume.delete()
        return {"deleted": resume.to_dict()}

    @oidc.accept_token(True, scopes_required=['resume:edit', 'resume:write', 'resume:admin'])
    @ns.expect(resume_json)
    def put(self, resume_id):
        resume = Resume.find_by(id=resume_id)
        if not resume:
            return {"error": "resume not found"}, 404

        resume = resume.update_and_save(**api.payload)
        return resume.to_dict(), 200


@application.route("/health")
def get(*args, **kw):
    return jsonify({"system": "ok"})
