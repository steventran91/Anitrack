import httpx
from unittest.mock import AsyncMock, Mock

def test_manga_search_success(client, monkeypatch):
    fake_anilist_response = {
        "data": {
            "Page": {
                "media": [
                    {
                        "id": 1,
                        "title": {"english": "Naruto", "native": "ナルト"},
                        "coverImage": {"large": "http://example.com/img.jpg"},
                        "chapters": 220,
                        "volumes": 10,
                        "status": "FINISHED",
                        "genres": ["Action"],
                        "averageScore": 79,
                    }
                ]
            }
        }
    }
    mock_search_manga = AsyncMock(return_value=fake_anilist_response)
    monkeypatch.setattr("app.api.routers.manga.search_manga", mock_search_manga)

    response = client.get("/manga?search=naruto")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["title_english"] == "Naruto"

def test_manga_search_unavailable(client, monkeypatch):
    mock_search_manga = AsyncMock(side_effect=httpx.HTTPError("AniList down"))
    monkeypatch.setattr("app.api.routers.manga.search_manga", mock_search_manga)

    response = client.get("/manga?search=naruto")
    assert response.status_code == 503

def test_manga_search_passes_pagination(client, monkeypatch):
    fake_anilist_response = {
        "data": {
            "Page": {
                "media": [
                    {
                        "id": 1,
                        "title": {"english": "Naruto", "native": "ナルト"},
                        "coverImage": {"large": "http://example.com/img.jpg"},
                        "chapters": 220,
                        "volumes": 10,
                        "status": "FINISHED",
                        "genres": ["Action"],
                        "averageScore": 79,
                    }
                ]
            }
        }
    }
    mock_manga_search = AsyncMock(return_value=fake_anilist_response)
    monkeypatch.setattr("app.api.routers.manga.search_manga", mock_manga_search)

    response = client.get("/manga?search=naruto&page=2&per_page=5")

    assert response.status_code == 200
    mock_manga_search.assert_called_with("naruto", page=2, per_page=5)

def test_manga_search_missing_params(client):
    response = client.get("/manga")
    assert response.status_code == 422

def test_manga_details_success(client, monkeypatch):
    fake_anilist_response = {
        "data": {
            "Media": {
                "id": 1,
                "title": {"english": "Berserk", "native": "ベルセルク"},
                "coverImage": {"large": "http://example.com/img.jpg"},
                "chapters": 364,
                "volumes": 41,
                "status": "RELEASING",
                "genres": ["Action"],
                "averageScore": 90,
                "description": "A dark fantasy story.",
                "bannerImage": "http://example.com/banner.jpg",
                "staff": {"nodes": [{"name": {"full": "Kentaro Miura"}}]},
            }
        }
    }
    mock_manga_detail = AsyncMock(return_value=fake_anilist_response)
    monkeypatch.setattr("app.api.routers.manga.get_manga_details", mock_manga_detail)

    response = client.get("/manga/1")

    assert response.status_code == 200 
    data = response.json()
    assert data["id"] == 1

def test_manga_not_found(client, monkeypatch):
    fake_response = Mock(status_code=404)
    error = httpx.HTTPStatusError("Not found", request=Mock(), response=fake_response)
    mock = AsyncMock(side_effect=error)
    monkeypatch.setattr("app.api.routers.manga.get_manga_details", mock)

    response = client.get("/manga/1")
    assert response.status_code == 404

def test_manga_detail_anilist_down(client, monkeypatch):
    mock_manga_details = AsyncMock(side_effect=httpx.RequestError("AniList down"))
    monkeypatch.setattr("app.api.routers.manga.get_manga_details", mock_manga_details)

    response = client.get("/manga/1")
    assert response.status_code == 503

