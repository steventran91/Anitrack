import httpx
from app.schemas.anime import AnimeSearchResult, MangaSearchResult, AnimeDetail

ANILIST_API_URL = "https://graphql.anilist.co"

SEARCH_ANIME_QUERY = """
query ($search: String, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
        }
        media(search: $search, type: ANIME) {
            id
            title {
                english
                native
            }
            coverImage {
                large
            }
            episodes
            status
            genres
            averageScore
        }
    }
}
"""

SEARCH_MANGA_QUERY = """
query ($search: String, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
        }
        media(search: $search, type: MANGA) {
            id
            title {
                english
                native
            }
            coverImage {
                large
            }
            chapters
            volumes
            status
            genres
            averageScore
        }
    }
}
"""

SEARCH_ANIME_DETAILS = """
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id
    title {
      english
      native
    }
    coverImage {
      large
    }
    episodes
    status
    genres
    averageScore
    description
    bannerImage
    studios {
      nodes {
        name
      }
    }
  }
}

"""

async def search_anime(search: str, page: int = 1, per_page: int = 20) -> dict:
    variables = {"search": search, "page": page, "perPage": per_page}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            ANILIST_API_URL,
            json={
                "query": SEARCH_ANIME_QUERY,
                "variables": variables,
            }
        )
        response.raise_for_status()
        return response.json()
    
def map_to_anime_search_results(raw_data: dict) -> list[AnimeSearchResult]:
    media_list = raw_data["data"]["Page"]["media"]

    results = []
    for media in media_list:
        results.append(
            AnimeSearchResult(
                id=media["id"],
                title_english=media["title"]["english"],
                title_native=media["title"]["native"],
                image=media["coverImage"]["large"],
                episodes=media["episodes"],
                status=media["status"],
                genres=media["genres"],
                average_score=media["averageScore"],
            )
        )
    return results 

async def search_manga(search: str, page: int = 1, per_page: int = 20) -> dict:
    variables = {"search": search, "page": page, "perPage": per_page}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            ANILIST_API_URL,
            json={
                "query": SEARCH_MANGA_QUERY,
                "variables": variables,
            },
        )
        response.raise_for_status()
        return response.json()
    
def map_to_manga_search_results(raw_data: dict) -> list[MangaSearchResult]:
    media_list = raw_data["data"]["Page"]["media"]

    results = []
    for media in media_list:
        results.append(
            MangaSearchResult(
                id=media["id"],
                title_english=media["title"]["english"],
                title_native=media["title"]["native"],
                image=media["coverImage"]["large"],
                chapters=media["chapters"],
                volumes=media["volumes"],
                status=media["status"],
                genres=media["genres"],
                average_score=media["averageScore"],
            )
        )
    return results

async def get_anime_details(anime_id: int) -> dict:
    variables = {"id": anime_id}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            ANILIST_API_URL,
            json={
                "query": SEARCH_ANIME_DETAILS,
                "variables": variables,
            }
        )
        response.raise_for_status()
        return response.json()
    
def map_to_anime_detail(raw_data: dict) -> AnimeDetail:
    media = raw_data["data"]["Media"]

    return  AnimeDetail(
                    id=media["id"],
                    description=media["description"],
                    banner_image=media["bannerImage"],
                    title_english=media["title"]["english"],
                    title_native=media["title"]["native"],
                    image=media["coverImage"]["large"],
                    episodes=media["episodes"],
                    status=media["status"],
                    genres=media["genres"],
                    average_score=media["averageScore"], 
                    studios=[studio["name"] for studio in media["studios"]["nodes"]]
            )
