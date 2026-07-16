import httpx
from unittest.mock import AsyncMock

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