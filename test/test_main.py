import pytest
from models import URL
from main import app
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

client = TestClient(app)

# Mocking the database session
@pytest.fixture
def mock_db_session():
    with patch('main.SessionLocal') as mock:
        mock.return_value = MagicMock()
        yield mock


# Test Get all urls by user
def test_read_all(mock_db_session):
    mock_db_session.return_value.query.return_value.all.return_value = [
        URL(id=1, title="Google", qrcode="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXIAAA", short_url="HBJbs34", 
            custom_alias=None, original_url="https://www.google.com/", clicks=3, 
            click_location=None, date_time_created="2024-03-12 14:45:47.183421", owner_id=1),

        URL(id=1, title="Facebook", qrcode="data:image/png;base64,bhbuhhsj8DXFCGSUjjjsus878HJ", short_url=None, 
            custom_alias="facebook", original_url="https://www.facebook.com/", clicks=1, 
            click_location=None, date_time_created="2024-03-11 18:12:20.175209", owner_id=1)
    ]
    response = client.get("/url/")
    assert response.status_code == 200
    assert len(response.json()) == 2



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
