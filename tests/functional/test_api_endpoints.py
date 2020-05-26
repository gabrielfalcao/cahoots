import vcr
import json
from .helpers import web_test



@web_test
@vcr.use_cassette('fixtures/vcr_cassettes/list-templates-v1-authz.yaml')
def test_list_templates(context):
    ("GET on /api/v1/templates/templates should return 200")

    # Given that I perform a GET /api/v1/templates/template
    response = context.http.get("/api/v1/templates/templates?access_token=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJVYjVzTjVPZzlsU2FYeUpzWWxrNXh2aE5sTEx3X3c5SGtaRUg3YlJub0U0In0.eyJqdGkiOiIwOWUzOGM4Ni0xYzczLTQxODMtOWYwNi1mMmUxMTJhZDI0MmIiLCJleHAiOjE1OTA0NjA3NDcsIm5iZiI6MCwiaWF0IjoxNTkwNDU5NTQ2LCJpc3MiOiJodHRwczovL2lkLnQubmV3c3RvcmUubmV0L2F1dGgvcmVhbG1zL2dhYnJpZWwtTkEtNDM5MjgiLCJzdWIiOiJlMjhmYWY1MC0yMWMyLTRlY2QtYjRhNi1jZDI2N2JjODY3M2UiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmYWtlLW5ld3N0b3JlLWFwaS12MSIsImF1dGhfdGltZSI6MTU5MDQ1OTU0Niwic2Vzc2lvbl9zdGF0ZSI6ImVjYTBmNjU2LWE1MWMtNDExNy1iMDI5LWQ5YWM5MTA3NzI0YSIsImFjciI6IjEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHRlbXBsYXRlOnJlYWQiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJzYWxlcy1hc3NvY2lhdGUgc2FsZXMtYXNzb2NpYXRlIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2FsZXMtYXNzb2NpYXRlIiwiZ2l2ZW5fbmFtZSI6InNhbGVzLWFzc29jaWF0ZSIsImZhbWlseV9uYW1lIjoic2FsZXMtYXNzb2NpYXRlIiwiZW1haWwiOiJzYWxlcy1hc3NvY2lhdGVAa2V5Y2xvYWsuZnVsbHRlc3QuY28ifQ.f-GSnZ3HKkaN98XSCzIYRbv-UVb-6YAd-0HZtlDFtmQOW-AXZz32eBHrZNVsZv65OtHGdZJ_pfG7dpudkDQhNqfhXXzUONnT9FlT196s42wyFzETN1OWU_DA_EycfcRXwPDlKY2OriGz1BmT224oP2i5Z2NWl-5HcBj_zsCYlR-2khx8VPq6VvMirxyL7MfSCW_YdBLzqCcvGKE8HQIXI9WKNBDq0beP-mPNbS5huzivDk61XGHEMQqa1z_ROu4X-GiDS24KA-1xH4Gpvx5lApQf3G33vQihboQAF7S-XjgsiblMvr62Ea7aFqi-olBeLlt5749U4SkCAGXyrRdBPQ")

    # When I check the response
    response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 401
    response.status_code.should.equal(200)


@web_test
@vcr.use_cassette('fixtures/vcr_cassettes/create-template-v1-anon.yaml')
def test_create_template_without_authentication(context):
    ("POST on /api/v1/templates/templates should return a json ")

    # Given that I perform a POST /api/v1/templates/template
    response = context.http.post(
        "/api/v1/templates/templates?access_token=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJVYjVzTjVPZzlsU2FYeUpzWWxrNXh2aE5sTEx3X3c5SGtaRUg3YlJub0U0In0.eyJqdGkiOiIwOWUzOGM4Ni0xYzczLTQxODMtOWYwNi1mMmUxMTJhZDI0MmIiLCJleHAiOjE1OTA0NjA3NDcsIm5iZiI6MCwiaWF0IjoxNTkwNDU5NTQ2LCJpc3MiOiJodHRwczovL2lkLnQubmV3c3RvcmUubmV0L2F1dGgvcmVhbG1zL2dhYnJpZWwtTkEtNDM5MjgiLCJzdWIiOiJlMjhmYWY1MC0yMWMyLTRlY2QtYjRhNi1jZDI2N2JjODY3M2UiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmYWtlLW5ld3N0b3JlLWFwaS12MSIsImF1dGhfdGltZSI6MTU5MDQ1OTU0Niwic2Vzc2lvbl9zdGF0ZSI6ImVjYTBmNjU2LWE1MWMtNDExNy1iMDI5LWQ5YWM5MTA3NzI0YSIsImFjciI6IjEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHRlbXBsYXRlOnJlYWQiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJzYWxlcy1hc3NvY2lhdGUgc2FsZXMtYXNzb2NpYXRlIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2FsZXMtYXNzb2NpYXRlIiwiZ2l2ZW5fbmFtZSI6InNhbGVzLWFzc29jaWF0ZSIsImZhbWlseV9uYW1lIjoic2FsZXMtYXNzb2NpYXRlIiwiZW1haWwiOiJzYWxlcy1hc3NvY2lhdGVAa2V5Y2xvYWsuZnVsbHRlc3QuY28ifQ.f-GSnZ3HKkaN98XSCzIYRbv-UVb-6YAd-0HZtlDFtmQOW-AXZz32eBHrZNVsZv65OtHGdZJ_pfG7dpudkDQhNqfhXXzUONnT9FlT196s42wyFzETN1OWU_DA_EycfcRXwPDlKY2OriGz1BmT224oP2i5Z2NWl-5HcBj_zsCYlR-2khx8VPq6VvMirxyL7MfSCW_YdBLzqCcvGKE8HQIXI9WKNBDq0beP-mPNbS5huzivDk61XGHEMQqa1z_ROu4X-GiDS24KA-1xH4Gpvx5lApQf3G33vQihboQAF7S-XjgsiblMvr62Ea7aFqi-olBeLlt5749U4SkCAGXyrRdBPQ",
        data=json.dumps(
            {"name": "test create template 1", "content": json.dumps({"some": "data"})}
        ),
        headers={"Content-Type": "application/json"},
    )

    # When I check the response
    response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 401
    response.status_code.should.equal(401)
