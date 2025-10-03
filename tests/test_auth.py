import pytest
from app.models.sql_models import User

def test_register_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }
    # First registration
    client.post("/auth/register", json=user_data)
    # Second registration should fail
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400

def test_login_user(client):
    # Register first
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass"
    }
    client.post("/auth/register", json=user_data)

    # Login
    login_data = {
        "username": "loginuser",
        "password": "loginpass"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    # Register first
    user_data = {
        "username": "wrongpass",
        "email": "wrong@example.com",
        "password": "correctpass"
    }
    client.post("/auth/register", json=user_data)

    # Login with wrong password
    login_data = {
        "username": "wrongpass",
        "password": "wrongpass"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 401