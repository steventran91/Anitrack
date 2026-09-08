from app.models.user import User
from app.models.anime import AnimeLibraryEntry, MangaLibraryEntry
from app.api.routers.auth import hash_password

def test_add_anime_to_library_success(client):
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Max",
            "last_name": "Tran",
            "email": "Maximus@gmail.com",
            "password": "Max123",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "auth/login",
        json={
            "email":"Maximus@gmail.com",
            "password": "Max123",
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.post(
        "/library/anime/",
        json={
            "anime_id": 21,
            "status": "watching",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["anime_id"] == 21
    assert data["status"] == "watching"

def test_add_anime_duplicate(client, auth_headers):
    response = client.post(
        "/library/anime/",
        json={
            "anime_id": 22,
            "status": "watching",
        },
        headers=auth_headers
    )
    assert response.status_code == 201

    response = client.post(
        "/library/anime/",
        json={
            "anime_id": 22,
            "status": "watching",
        },
        headers=auth_headers
    )
    assert response.status_code == 400

def test_list_anime_library_only_returns_own_entries(client, db_session, auth_headers):
    other_user = User(
        first_name="Other",
        last_name="User",
        email="other@example.com",
        hashed_password=hash_password("password123"),
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_entry = AnimeLibraryEntry(
        user_id=other_user.id,
        anime_id=999,
        status="watching",
    )
    db_session.add(other_entry)
    db_session.commit()

    response = client.post(
        "/library/anime/",
        json={
            "anime_id": 22,
            "status": "watching",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["anime_id"] == 22

    response = client.get("/library/anime", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["anime_id"] == 22

def test_update_anime_library_entry(client, auth_headers):
    response = client.post(
        "/library/anime",
        json={
            "anime_id": 22,
            "status": "watching",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.patch(
        "/library/anime/22",
        json={
            "status": "completed",
            "current_episode": 100,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["current_episode"] == 100

def test_update_nonexistent_entry(client, auth_headers):
    response = client.patch(
        "/library/anime/1000",
        json={
            "status": "dropped",
            "current_episode": "2",
        },
        headers=auth_headers
    )
    assert response.status_code == 404

def test_delete_anime_library_entry(client, auth_headers):
    response = client.post(
        "/library/anime",
        json={
            "anime_id": 25,
            "current_episode": 10,
        },
        headers=auth_headers
    )
    assert response.status_code == 201

    response = client.delete("/library/anime/25", headers=auth_headers)
    assert response.status_code == 204

def test_anime_library_requires_auth(client):
    response = client.post(
        "/library/anime",
        json={
            "anime_id": 20,
            "current_episode": 3,
        },
    )
    assert response.status_code == 401

def test_add_manga_to_library(client):


    response = client.post(
        "/auth/register",
        json={
            "first_name": "Max",
            "last_name": "Tran",
            "email": "Maximus@gmail.com",
            "password": "Max123",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "Maximus@gmail.com",
            "password": "Max123",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.post(
        "/library/manga",
        json={
            "manga_id": 21,
            "status": "reading",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["manga_id"] == 21
    assert data["status"] == "reading"

def test_add_manga_duplicate(client, auth_headers):
    response = client.post(
        "/library/manga",
        json={
            "manga_id": 21,
            "status": "reading",
        },
        headers=auth_headers
    )
    assert response.status_code == 201

    response = client.post(
        "/library/manga",
        json={
            "manga_id": 21,
            "status": "reading",
        },
        headers=auth_headers,
    )

    assert response.status_code == 400

def test_list_manga_library_only_return_own_entries(client, db_session, auth_headers):
    other_user = User(
        first_name="Other",
        last_name="User",
        email="other@example.com",
        hashed_password=hash_password("password123"),
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_entry = MangaLibraryEntry(
        user_id=other_user.id,
        manga_id=999,
        status="reading",
    )
    db_session.add(other_entry)
    db_session.commit()

    response = client.post(
        "/library/manga",
        json={
            "manga_id": 22,
            "status": "reading",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["manga_id"] == 22

    response = client.get(
        "/library/manga",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["manga_id"] == 22

def test_update_manga_library_entry(client, auth_headers):
    response = client.post(
        "/library/manga",
        json={
            "manga_id": 98,
            "status": "reading",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.patch(
        "/library/manga/98",
        json={
            "status": "completed",
            "current_chapter": 100,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["current_chapter"] == 100

def test_update_nonexistent_manga_entry(client, auth_headers):

    response = client.patch(
        "/library/manga/100",
        json={
            "status": "dropped"
        },
        headers=auth_headers,
    )
    assert response.status_code == 404

def test_delete_manga_entry(client, auth_headers):
    response = client.post(
        "/library/manga",
        json={
            "manga_id": 100,
            "status": "reading",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201 

    response = client.delete(
        "/library/manga/100",
        headers=auth_headers,
    )
    assert response.status_code == 204

def test_manga_library_requires_auth(client):
    response = client.post(
        "/library/manga",
        json={
            "manga_id": 20,
            "status": "reading",
        }
    )
    assert response.status_code == 401