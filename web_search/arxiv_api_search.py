import requests
import feedparser

ARXIV_URL = "http://export.arxiv.org/api/query"

def search_arxiv(query, max_results = 10) -> list[str]:
    """Request files that match the query using the arXiv API.

    Returns:
        _type_: _description_
    """
    
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    response = requests.get(ARXIV_URL, params=params)
    feed = feedparser.parse(response.text)
    results = [entry.id.replace("abs", "pdf") for entry in feed.entries]
    return results