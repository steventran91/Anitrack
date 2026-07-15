import httpx

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

async def search_anime(search: str, page: int = 1, per_page: int = 20) -> dict:
    variables = {"search": search, "page": page, "perPage": per_page}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            ANILIST_API_URL,
            json={
                "query": SEARCH_ANIME_QUERY,
                "variables": variables,
            }
        )
        response.raise_for_status()
        return response.json()