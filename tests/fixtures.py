import pytest as pt

from api import create_app
from api.v1.models import db


@pt.fixture(scope="class")
def api_test_client(request):
    class TestCaseHook:
        pass

    request.cls.app = create_app(configName="test")
    request.cls.context = request.cls.app.app_context()
    request.cls.context.push()
    db.create_all()
    request.cls.client = request.cls.app.test_client()
    yield
    db.session.remove()
    db.drop_all()
    request.cls.context.pop()