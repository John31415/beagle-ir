from data_ingestion.crawlers.arxiv_crawler import arxiv_crawler
from data_ingestion.scrappers.arxiv_scrapper import ArxivScrapper
from utils.utils import RobotsParser, time_since_creation_files, delete_file, download_file

def create_corpus():
    base_url = "https://arxiv.org"
    robots_url = base_url + "/robots.txt"
    robots_parser = RobotsParser(robots_url)
    robots_parser.parse_robots_txt()
    field_urls = arxiv_crawler(robots_parser)
    print(len(field_urls), " Field URLs obtained.")
    scrapper = ArxivScrapper()
    scrapper.arxiv_scrapper(robots_parser, field_urls, 25, "corpus")

def update_corpus(total_docs: int):
    """Replace old documents with new ones.

    Args:
        total_docs (int): Number of documents to replace.
    """
    base_url = "https://arxiv.org"
    robots_url = base_url + "/robots.txt"
    robots_parser = RobotsParser(robots_url)
    robots_parser.parse_robots_txt()
    field_urls = arxiv_crawler(robots_parser)
    scrapper = ArxivScrapper()
    cnt = 0
    for (field_name, field_url) in field_urls:
        if total_docs == cnt:
            break
        print(field_name)
        pdf_urls = scrapper.get_pdf_urls(robots_parser, field_url, total_docs)
        for pdf in pdf_urls:
            if total_docs == cnt:
                break
            print(pdf)
            if download_file("corpus", pdf, robots_parser.get_delay()):
                cnt += 1
        old_files = time_since_creation_files("corpus")[:cnt]
        for (file, _) in old_files:
            delete_file("corpus", file)

update_corpus(5)