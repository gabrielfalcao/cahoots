# import vcr
import json
from .helpers import web_test


# @vcr.use_cassette('fixtures/vcr_cassettes/test_list_templates.yaml')
@web_test
def test_list_templates_without_authentication(context):
    ("GET on /api/v1/templates/templates should return 401")

    # Given that I perform a GET /api/v1/templates/template
    response = context.http.get("/api/v1/templates/templates")

    # When I check the response
    response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 401
    response.status_code.should.equal(401)


@web_test
def test_create_template(context):
    ("POST on /api/v1/templates/templates should return a json ")

    # Given that I perform a POST /api/v1/templates/template
    response = context.http.post(
        "/api/v1/templates/templates",
        data=json.dumps(
            {"name": "test create template 1", "content": json.dumps({"some": "data"})}
        ),
        headers={"Content-Type": "application/json"},
    )

    # When I check the response
    response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 201
    response.status_code.should.equal(201)
