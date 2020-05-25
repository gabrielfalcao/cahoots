import json
from .helpers import web_test


@web_test
def test_keycloak_admin_push_get(context):
    ("GET on /auth/admin should return 200")

    response = context.http.get("/auth/admin")

    # # When I check the response
    # response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 200
    response.status_code.should.equal(200)


@web_test
def test_keycloak_admin_push_post(context):
    ("POST on /auth/admin should return 200")

    response = context.http.post("/auth/admin/k_push_not_before")

    # # When I check the response

    # And check if the status was 200
    response.status_code.should.equal(200)

    response = context.http.get("/api/v1/admin-requests")
    response.status_code.should.equal(200)
    response.headers.should.have.key("Content-Type").being.equal("application/json")
    json.loads(response.data).should.have.length_of(1)
