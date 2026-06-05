from web_search.arxiv_api_search import search_arxiv
from utils.text_processor import TextPreprocessor
from data_ingestion.utils.files import store_url_corpus
from data_ingestion.utils.urls import download_file
from data_ingestion.utils.robots import RobotsParser
from utils.hash import hash_str
from indexing.build_indexes import add2index

def _download(pdfs_urls: list[str], crawl_delay: int):
    for url in pdfs_urls:
        store_url_corpus(url, "corpus_urls.txt")
        if download_file("corpus", url, crawl_delay):
            store_url_corpus(url, "downloaded_urls.txt")

def web_search(query: str, search_limit: int) -> list[str]:
    """Method for finding articles that match the query on the web.
    """

    print("Searching the web")
    robots_parser = RobotsParser("https://arxiv.org/robots.txt")
    robots_parser.parse_robots_txt()
    crawl_delay = robots_parser.get_delay()
    tp = TextPreprocessor(query)
    query_tokens = tp.get_normalized_tokens()
    query_processed = " ".join(query_tokens)
    pdfs_urls = search_arxiv(query_processed, search_limit)
    _download(pdfs_urls, crawl_delay)
    pdfs_hash = [hash_str(url) for url in pdfs_urls]
    add2index(pdfs_urls)
    return pdfs_hash