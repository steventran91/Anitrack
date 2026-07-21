import httpx
from unittest.mock import AsyncMock, Mock

def test_anime_search_success(client, monkeypatch):
    fake_anilist_response = {
        "data": {
            "Page": {
                "media": [
                    {
                        "id": 1,
                        "title": {"english": "Naruto", "native": "ナルト"},
                        "coverImage": {"large": "http://example.com/img.jpg"},
                        "episodes": 220,
                        "status": "FINISHED",
                        "genres": ["Action"],
                        "averageScore": 79,
                    }
                ]
            }
        }
    }

    mock_search_anime = AsyncMock(return_value=fake_anilist_response)
    monkeypatch.setattr("app.api.routers.anime.search_anime", mock_search_anime)

    response = client.get("/anime?search=naruto")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["title_english"] == "Naruto"

def test_anime_search_unavailable(client, monkeypatch):
    mock_search_anime = AsyncMock(side_effect=httpx.HTTPError("AniList down"))
    monkeypatch.setattr("app.api.routers.anime.search_anime", mock_search_anime)

    response = client.get("/anime?search=naruto")
    assert response.status_code == 503

def test_anime_search_passes_pagination(client, monkeypatch):
    fake_anilist_response = {
        "data": {
            "Page": {
                "media": [
                    {
                        "id": 1,
                        "title": {"english": "Naruto", "native": "ナルト"},
                        "coverImage": {"large": "http://example.com/img.jpg"},
                        "episodes": 220,
                        "status": "FINISHED",
                        "genres": ["Action"],
                        "averageScore": 79,
                    }
                ]
            }
        }
    }
    mock_anime_search = AsyncMock(return_value=fake_anilist_response)
    monkeypatch.setattr("app.api.routers.anime.search_anime", mock_anime_search)

    response = client.get("/anime?search=naruto&page=2&per_page=5")

    assert response.status_code == 200
    mock_anime_search.assert_called_with("naruto", page=2, per_page=5)

def test_anime_search_missing_params(client):
    response = client.get("/anime")
    assert response.status_code == 422

def test_anime_details_success(client, monkeypatch):
    fake_anilist_response = {
        "data": {
            "Media": {
                "id": 1,
                "title": {"english": "Naruto", "native": "ナルト"},
                "coverImage": {"large": "http://example.com/img.jpg"},
                "episodes": 220,
                "status": "FINISHED",
                "genres": ["Action"],
                "averageScore": 79,
                "description": "A ninja story.",
                "bannerImage": "http://example.com/banner.jpg",
                "studios": {"nodes": [{"name": "Studio Pierrot"}]},
            }
        }
    }
    mock_anime_detail = AsyncMock(return_value=fake_anilist_response)
    monkeypatch.setattr("app.api.routers.anime.get_anime_details", mock_anime_detail)

    response = client.get("/anime/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_anime_details_not_found(client, monkeypatch):
    fake_response = Mock(status_code=404)
    error = httpx.HTTPStatusError("Not found", request=Mock(), response=fake_response)
    mock = AsyncMock(side_effect=error)
    monkeypatch.setattr("app.api.routers.anime.get_anime_details", mock)

    response = client.get("/anime/1")
    assert response.status_code == 404

