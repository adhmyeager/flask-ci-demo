import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_index_returns_200(client):
    res = client.get('/')
    assert res.status_code == 200

def test_health_endpoint(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'ok'

def test_greet_endpoint(client):
    res = client.get('/greet/World')
    assert res.status_code == 200
    assert 'Hello, World!' in res.get_json()['message']