from app import app

def test_healthcheck():
    client = app.test.client()
    response = client.get('/')
    assert response.status_code == 200