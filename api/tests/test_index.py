from starlette.testclient import TestClient
import os
os.environ['BGC_USERNAME'] = 'testuser'
os.environ['BGC_PASSWORD'] = 'testpass'

from api.index import app
import pytest
from aioresponses import aioresponses

@pytest.fixture
def bgc_api():
    with aioresponses() as api:
        api.post('/login.jsp', status=200, body='ok')
        api.post('/Json', status=200, body='[]', repeat=True)
        yield api

@pytest.fixture
def client():
    return TestClient(app)


def test_homepage_returns_success(client, bgc_api):
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_passes_required_context(client, bgc_api):
    response = client.get('/')
    assert 'games' in response.context
