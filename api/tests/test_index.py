from starlette.testclient import TestClient

from api.index import app

def test_homepage_returns_success():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_passes_required_context():
    client = TestClient(app)
    response = client.get('/')
    assert 'games' in response.context
