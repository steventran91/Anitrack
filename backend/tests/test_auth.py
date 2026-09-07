def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "hashed_password" not in data
    assert "password" not in data

def test_register_duplicate_email(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Naruto",
            "last_name": "Uzumaki",
            "email": "uzumaki@gmail.com",
            "password": "believeit!",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "uzumaki@gmail.com"

    dupe_email_response = client.post(
        "/auth/register",
        json={
            "first_name": "Boruto",
            "last_name": "Uzumaki",
            "email": "uzumaki@gmail.com",
            "password": "believeit!",
        },
    )
    assert dupe_email_response.status_code == 400

def test_login_success(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Sasuke",
            "last_name": "Uchiha",
            "email": "uchiha@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "uchiha@gmail.com",
            "password": "password123",
        },
    )
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data

def test_login_wrong_password(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Sasuke",
            "last_name": "Uchiha",
            "email": "uchiha@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201

    wrong_password_response = client.post(
        "/auth/login",
        json={
            "email": "uchiha@gmail.com",
            "password": "password1234",
        },
    )
    assert wrong_password_response.status_code == 401

def test_login_nonexistent_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "newemail@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == 401

def test_me_with_valid_token(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Luffy",
            "last_name": "Monkey",
            "email": "pirateking@gmail.com",
            "password": "theonepiece",
        },
    )
    assert response.status_code == 201
    registered_id = response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json={
            "email": "pirateking@gmail.com",
            "password": "theonepiece",
        },
    )
    assert login_response.status_code == 200 
    token = login_response.json()["access_token"]

    token_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert token_response.status_code == 200 
    data = token_response.json()
    assert data["id"] == registered_id
    assert data["email"] == "pirateking@gmail.com"
    assert data["first_name"] == "Luffy"
    assert data["last_name"] == "Monkey"

def test_me_without_token(client):
    response = client.get(
        "/auth/me",
    )
    assert response.status_code == 401

def test_me_with_invalid_token(client):
    token = '123;oaiejf;oiwej3'
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    