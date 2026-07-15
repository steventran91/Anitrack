from unittest.mock import AsyncMock

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