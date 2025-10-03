import pytest

def test_create_item(client):
    # Register and login user
    user_data = {
        "username": "itemuser",
        "email": "item@example.com",
        "password": "itempass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "itemuser", "password": "itempass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    item_data = {
        "title": "Test Item",
        "description": "A test item"
    }
    response = client.post("/api/items/", json=item_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "A test item"
    assert data["owner_id"] == 1  # Assuming first user

def test_read_items(client):
    # Register and login user
    user_data = {
        "username": "readuser",
        "email": "read@example.com",
        "password": "readpass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "readuser", "password": "readpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create item
    item_data = {"title": "Read Item", "description": "Item to read"}
    client.post("/api/items/", json=item_data, headers=headers)

    # Read items
    response = client.get("/api/items/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Read Item"

def test_update_item(client):
    # Register and login user
    user_data = {
        "username": "updateuser",
        "email": "update@example.com",
        "password": "updatepass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "updateuser", "password": "updatepass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create item
    item_data = {"title": "Original Item", "description": "Original description"}
    create_response = client.post("/api/items/", json=item_data, headers=headers)
    item_id = create_response.json()["id"]

    # Update item
    update_data = {"title": "Updated Item", "description": "Updated description"}
    response = client.put(f"/api/items/{item_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"
    assert data["description"] == "Updated description"

def test_delete_item(client):
    # Register and login user
    user_data = {
        "username": "deleteuser",
        "email": "delete@example.com",
        "password": "deletepass"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/token", data={"username": "deleteuser", "password": "deletepass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create item
    item_data = {"title": "Delete Item", "description": "Item to delete"}
    create_response = client.post("/api/items/", json=item_data, headers=headers)
    item_id = create_response.json()["id"]

    # Delete item
    response = client.delete(f"/api/items/{item_id}", headers=headers)
    assert response.status_code == 200

    # Verify deletion
    response = client.get(f"/api/items/{item_id}", headers=headers)
    assert response.status_code == 404