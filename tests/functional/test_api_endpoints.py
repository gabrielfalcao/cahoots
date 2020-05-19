import vcr
from .helpers import web_test


@vcr.use_cassette('fixtures/vcr_cassettes/test_list_resumes.yaml')
@web_test
def test_list_resumes(context):
    ("GET on /api/v1/resume should return a json containing hello world")

    # Given that I perform a GET /api/v1/resume
    response = context.http.get("/api/v1/resume")

    import ipdb;ipdb.set_trace()
    # When I check the response
    response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 200
    response.status_code.should.equal(200)
