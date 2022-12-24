from starlette.testclient import TestClient

from api.index import app

def test_homepage():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    
