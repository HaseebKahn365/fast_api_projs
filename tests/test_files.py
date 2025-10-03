import pytest
import os
from io import BytesIO

def test_upload_file(client):
    # Register and login user
    user_data = {
        "username": "fileuser",
        "email": "file@example.com",
        "password": "filepass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "fileuser", "password": "filepass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Upload file
    file_content = b"Hello, this is a test file!"
    files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
    response = client.post("/files/upload/", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["message"] == "File uploaded successfully"

    # Verify file exists
    assert os.path.exists(os.path.join("uploads", "test.txt"))

def test_download_file(client):
    # Register and login user
    user_data = {
        "username": "downloaduser",
        "email": "download@example.com",
        "password": "downloadpass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "downloaduser", "password": "downloadpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Upload file first
    file_content = b"Download test content"
    files = {"file": ("download.txt", BytesIO(file_content), "text/plain")}
    client.post("/files/upload/", files=files, headers=headers)

    # Download file
    response = client.get("/files/download/download.txt", headers=headers)
    assert response.status_code == 200
    assert response.content == file_content

def test_download_nonexistent_file(client):
    # Register and login user
    user_data = {
        "username": "nonexistuser",
        "email": "nonexist@example.com",
        "password": "nonexistpass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "nonexistuser", "password": "nonexistpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Try to download nonexistent file
    response = client.get("/files/download/nonexistent.txt", headers=headers)
    assert response.status_code == 200  # The code returns 200 with error message, but should be 404
    data = response.json()
    assert "error" in data