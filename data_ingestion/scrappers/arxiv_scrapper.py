from data_ingestion.utils.robots import RobotsParser
from data_ingestion.utils.urls import get_urls, download_file
from data_ingestion.utils.files import count_files, store_url_corpus
from data_ingestion.utils.arxiv import valid_query_arxiv
from utils.files import read_urls_corpus
import time

class ArxivScrapper:
    """Set of methods to find and download papers from arXiv.org
    """

    def __init__(self):
        self.base_url = "https://arxiv.org"
        self.robots_url = self.base_url + "/robots.txt"

    def get_pdf_urls(self, robots_parser: RobotsParser, url: str, top_k: int) -> list[str]:
        """Find the k most recent URLs of papers at a given URL

        Args:
            robots_parser (RobotsParser): robots.txt parser
            url (str): URL of the given page 
            top_k (int): number of papers to find.

        Returns:
            list[str]: list of founded URLs
        """

        valid_preffix = self.base_url + "/pdf"
        all_urls = get_urls(url)
        allowed_urls = list(filter(
            lambda url: robots_parser.is_allowed(url[1]),
            all_urls
        ))
        valid_urls = list(filter(
            lambda url: url[1].startswith(valid_preffix),
            allowed_urls
        ))
        return [x[1] for x in valid_urls[:top_k]]
    
    def _download_pdfs(self, corpus_path: str, corpus_urls: str, crawl_delay: float, limit_pdfs = 2000):
        """Download a given list of files at a path with some delay.

        Args:
            corpus_path (str): path of the corpus
            corpus_urls (str): path of the txt with urls
            crawl_delay (float): delay
            limit_pdfs (int): limit of PDF files that can be stored in the corpus
        """
        
        urls = read_urls_corpus(corpus_urls)
        for url in urls:
            if count_files(corpus_path) >= limit_pdfs:
                return
            if download_file(corpus_path, url, crawl_delay):
                store_url_corpus(url, "downloaded_urls.txt")

    def arxiv_scrapper(self, robots_parser: RobotsParser, urls: list[tuple[str, str]], top_k: int, corpus_path: str):
        """Download the top_k most recent papers from each field obtained from arxiv_crawler

        Args:
            robots_parser (RobotsParser): robots.txt parser
            urls (list[tuple[str, str]]): list of tuples (Field name, URL)
            top_k (int, optional): number of papers to download. Defaults to 10.
            corpus_path (str, optional): path of the corpus file parent. Defaults to "..".

        Returns:
            _type_: _description_
        """

        print("Arxiv Scrapper Starting")
        pdf_urls = []
        crawl_delay = robots_parser.get_delay()
        for (field_name, url) in urls:
            url_top_k = url + f"?skip=0&show={valid_query_arxiv(top_k)}"
            time.sleep(crawl_delay)
            field_pdf_urls = self.get_pdf_urls(robots_parser, url_top_k, top_k)
            pdf_urls += field_pdf_urls
            for field_url in field_pdf_urls:
                store_url_corpus(field_url, "corpus_urls.txt")
        self._download_pdfs(corpus_path, "corpus_urls.txt", crawl_delay)