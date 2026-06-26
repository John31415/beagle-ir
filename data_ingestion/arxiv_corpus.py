from data_ingestion.crawlers.arxiv_crawler import arxiv_crawler
from data_ingestion.scrappers.arxiv_scrapper import ArxivScrapper
from data_ingestion.utils.robots import RobotsParser
from data_ingestion.utils.urls import download_file

def create_corpus(max_files: int = 2000):
    base_url = "https://arxiv.org"
    robots_url = base_url + "/robots.txt"
    robots_parser = RobotsParser(robots_url)
    robots_parser.parse_robots_txt()
    field_urls = arxiv_crawler(robots_parser, max_links=max_files)
    print(len(field_urls), " Field URLs obtained.")
    scrapper = ArxivScrapper()
    scrapper.arxiv_scrapper(robots_parser, field_urls, 25, "corpus", max_files)

# create_corpus()
# python3 -m data_ingestion.arxiv_corpus