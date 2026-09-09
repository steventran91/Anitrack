from app.models.user import User
from app.models.anime import AnimeLibraryEntry, MangaLibraryEntry
from app.api.routers.auth import hash_password
# test_dashboard_requires_auth

def test_dashboard_returns_watching_and_reading(client, auth_headers):
    response = client.post(
        "/library/anime",
        json={
            "anime_id": 22,
            "status": "watching",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201 

    response = client.post(
        "/library/manga",
        json={
            "manga_id": 23,
            "status": "reading",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.get(
        "/dashboard",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["continue_watching"]) == 1
    assert len(data["continue_reading"]) == 1
    assert data["continue_watching"][0]["anime_id"] == 22
    assert data["continue_reading"][0]["manga_id"] == 23

def test_dashboard_excludes_other_statuses(client, auth_headers):
    response = client.post(
        "/library/anime",
        json={
            "anime_id": 22,
            "status": "completed",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201 

    response = client.post(
        "/library/anime",
        json={
            "anime_id": 23,
            "status": "watching",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.get(
        "/dashboard",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["continue_watching"]) == 1
    assert data["continue_watching"][0]["anime_id"] == 23

def test_dashboard_only_returns_own_entries(client, db_session, auth_headers):
    other_user = User(
        first_name="Max",
        last_name="Tran",
        email="Max@gmail.com",
        hashed_password=hash_password("Max123"),
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
        "/library/anime",
        json={
            "anime_id": 1,
            "status": "watching",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.post(
        "/library/manga",
        json={
            "manga_id": 2,
            "status": "reading",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.get(
        "/dashboard",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["continue_watching"]) == 1
    assert len(data["continue_reading"]) == 1
    assert data["continue_watching"][0]["anime_id"] == 1
    assert data["continue_reading"][0]["manga_id"] == 2

def test_dashboard_requires_auth(client):
    response = client.get(
        "/dashboard",
    )
    assert response.status_code == 401