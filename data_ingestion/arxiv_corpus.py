from data_ingestion.crawlers.arxiv_crawler import arxiv_crawler
from data_ingestion.scrappers.arxiv_scrapper import ArxivScrapper
from data_ingestion.utils.robots import RobotsParser
from data_ingestion.utils.urls import download_file

def create_corpus():
    base_url = "https://arxiv.org"
    robots_url = base_url + "/robots.txt"
    robots_parser = RobotsParser(robots_url)
    robots_parser.parse_robots_txt()
    field_urls = arxiv_crawler(robots_parser)
    print(len(field_urls), " Field URLs obtained.")
    scrapper = ArxivScrapper()
    scrapper.arxiv_scrapper(robots_parser, field_urls, 25, "corpus")