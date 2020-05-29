from sure import scenario
from cahoots.config import dbconfig
from cahoots.web import application
from chemist import set_default_uri, metadata


def before_each_test(context):
    context.web = application
    context.http = context.web.test_client()
    # engine = set_default_uri(dbconfig.sqlalchemy_url())
    metadata.drop_all()
    metadata.create_all()

    with context.http.session_transaction() as session:
        session["jwt_payload"] = {"user": {"name": "foo bar"}}


def after_each_test(context):
    # I would clean up the database here, if I had one
    pass


web_test = scenario(before_each_test, after_each_test)
