from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_home():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == 'home.html'
    assert "request" in response.context


def test_auth_signup():
    client = TestClient(app)
    response = client.get("/auth/signup")
    assert response.status_code == 200
    assert response.template.name == 'signup.html'
    assert "request" in response.context


def test_auth_login():
    client = TestClient(app)
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert response.template.name == 'login.html'
    assert "request" in response.context
