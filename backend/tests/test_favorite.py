from app.models.user import User
from app.models.favorite import Favorite, FavoriteType
from app.api.routers.auth import hash_password

def test_add_favorite_success(client, auth_headers):
    response = client.post(
        "/favorites",
        json={
            "item_type": "anime",
            "item_id": 20,
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item_type"] == "anime"
    assert data["item_id"] == 20

def test_add_favorite_duplicate(client, auth_headers):
    response = client.post(
        "/favorites",
        json={
            "item_type": "manga",
            "item_id": 23,
        },
        headers=auth_headers
    )
    assert response.status_code == 201

    response = client.post(
        "/favorites",
        json={
            "item_type": "manga",
            "item_id": 23,
        },
        headers=auth_headers
    )
    assert response.status_code == 400

def test_list_favorites_only_returns_own_entries(client, db_session, auth_headers):
    other_user = User(
        first_name="Bao",
        last_name="Chu",
        email="bao@gmail.com",
        hashed_password=hash_password("bao123"),
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_favorite = Favorite(
        user_id=other_user.id,
        item_type="anime",
        item_id=2,
    )
    db_session.add(other_favorite)
    db_session.commit()

    response = client.post(
        "/favorites",
        json={
            "item_type": "manga",
            "item_id": 20,
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["item_id"] == 20

    response = client.get(
        "/favorites", 
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["item_id"] == 20

def test_delete_favorite(client, auth_headers):
    response = client.post(
        "/favorites",
        json={
            "item_type": "manga",
            "item_id": 20,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201

    response = client.delete(
        "/favorites/manga/20",
        headers=auth_headers
    )
    assert response.status_code == 204

def test_favorite_requires_auth(client):
    response = client.post(
        "/favorites",
        json={
            "item_type": "manga",
            "item_id": 20,
        }
    )
    assert response.status_code == 401
