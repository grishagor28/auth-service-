import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_success():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_register_duplicate():
    client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "testpass123"
    })
    response = client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "testpass123"
    })
    assert response.status_code == 400


def test_login_success():
    client.post("/auth/register", json={
        "username": "loginuser",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    client.post("/auth/register", json={
        "username": "wrongpassuser",
        "password": "correctpass"
    })
    response = client.post("/auth/login", json={
        "username": "wrongpassuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_get_me():
    client.post("/auth/register", json={
        "username": "meuser",
        "password": "testpass123"
    })
    login_response = client.post("/auth/login", json={
        "username": "meuser",
        "password": "testpass123"
    })
    token = login_response.json()["access_token"]
    response = client.get("/auth/me", headers={
        "Authorization": "Bearer " + token
    })
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"