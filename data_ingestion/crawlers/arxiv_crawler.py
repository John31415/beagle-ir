from collections import deque
from urllib.parse import urlparse
from data_ingestion.utils.robots import RobotsParser
from data_ingestion.utils.urls import get_urls


def arxiv_crawler(
    robots_parser: RobotsParser,
    start_url: str = "https://arxiv.org",
    max_depth: int = 2,
    max_links: int = 100,
) -> list[tuple[str, str]]:
    """
    Crawler that extracts URLs from arXiv using the BFS algorithm.
    Args:
        robots_parser: Instance to validate robots.txt permissions.
        start_url: Initial URL from which crawling will begin.
        max_depth: Maximum search depth.
        max_links: Maximum number of unique links to extract and return.
    """
    print(f"BFS Crawler: {start_url}")
    print(f"Settings -> Max Depth: {max_depth} | Limit URLs: {max_links}")
    parsed_start = urlparse(start_url)
    base_domain = f"{parsed_start.scheme}://{parsed_start.netloc}"
    queue = deque([(start_url, 0)])
    visited_urls = set([start_url])
    extracted_links = []
    if not robots_parser.is_allowed(start_url):
        return extracted_links
    while queue and len(extracted_links) < max_links:
        current_url, current_depth = queue.popleft()
        if current_depth >= max_depth:
            continue
        try:
            discovered_urls = get_urls(current_url)
        except Exception as e:
            print(f"Error tracking {current_url}: {e}")
            continue
        for name, link in discovered_urls:
            if len(extracted_links) >= max_links:
                break
            if not link.startswith(base_domain):
                continue
            if link in visited_urls:
                continue
            if not robots_parser.is_allowed(link):
                continue
            visited_urls.add(link)
            extracted_links.append((name, link))
            if current_depth + 1 < max_depth:
                queue.append((link, current_depth + 1))

    def suffix_order(item: tuple[str, str]) -> int:
        url = item[1]
        if url.endswith("/new"):
            return 0
        elif url.endswith("/recent"):
            return 1
        return 2

    extracted_links.sort(key=suffix_order)
    top_links = 5
    print(f"Top {top_links} URLs:")
    for l in extracted_links[:top_links]:
        print(l)
    return extracted_links
