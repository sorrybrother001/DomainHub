import pytest
from manage import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"DomainHub" in r.data