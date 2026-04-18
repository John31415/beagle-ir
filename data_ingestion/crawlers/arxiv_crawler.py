from data_ingestion.utils.robots import RobotsParser
from data_ingestion.utils.urls import get_urls

def arxiv_crawler(robots_parser: RobotsParser) -> list[tuple[str, str]]:
    """It retrieves the URLs of the pages for each specific scientific field from arXiv. 

    Returns:
    list[tuple[str, str]]: List of tuples (Field name, URL)
    """

    print("Arxiv Crawler Starting")
    base_url = "https://arxiv.org"
    valid_preffix = "https://arxiv.org/list"
    valid_suffix = "/recent"
    all_urls = get_urls(base_url)
    print("All URLs Crawled")
    print(all_urls)
    allowed_urls = list(filter(
        lambda url: robots_parser.is_allowed(url[1]), 
        all_urls))
    valid_urls = list(filter(
        lambda url: url[1].startswith(valid_preffix) and 
        url[1].endswith(valid_suffix), 
        allowed_urls))
    return valid_urls