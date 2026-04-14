def extract_path(url: str) -> str:
    """Extracts the path from a URL

    Examples:
        >>> extract_path("https://arxiv.org/pdf/2604.08260")
        "/pdf/2604.08260"
    """

    from urllib.parse import urlparse

    parsed = urlparse(url)
    return parsed.path if parsed.path else "/"

class RobotsParser:
    """Provides methods to process robots.txt
    """

    from urllib.robotparser import RobotFileParser

    def __init__(self, robots_url):
        self.robots_url = robots_url
        self.user_agent = 'bot'

    def parse_robots_txt(self):
        print(f"Parsing robots.txt at {self.robots_url}")
        self.rp = self.RobotFileParser()
        self.rp.set_url(self.robots_url)
        self.rp.read()
        print("robots.txt parsed")
    
    def is_allowed(self, path) -> bool:
        return self.rp.can_fetch(self.user_agent, path)
    
    def get_delay(self) -> float:
        return self.rp.crawl_delay(self.user_agent)
    
def get_urls(url: str) -> list[tuple[str, str]]:
    """Extracts all URLs from a page

    Returns:
        list[tuple[str, str]]: List of tuples (Anchor text, URL)
    """
    
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        urls = []
        for link in soup.find_all('a', href=True):
            anchor_text = link.get_text(strip = True)
            link_j = urljoin(url ,link['href'])
            if anchor_text == "recent":
                container = link.find_parent()
                category_tag = container.find('a')
                anchor_text = category_tag.get_text(strip = True) if category_tag else "Unknown"
            urls.append((anchor_text, link_j))
        return urls

    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return []
    
def valid_query_arxiv(k: int) -> int:
    """Returns the lowest value greater than k that is valid for requests in arXiv.
    """
    valid_values = [25, 50, 100, 250, 500, 1000, 2000]
    for vv in valid_values:
        if k <= vv:
            return vv
    return valid_values[-1]

def hash_str(string: str) -> str:
    """Compute the md5 hash of a string. 

    Returns:
        str: Hexadecimal digits of the hash.
    """

    import hashlib

    return hashlib.md5(string.encode()).hexdigest()

def download_file(path: str, url: str, delay: float) -> bool:
    """Download the file from a given URL to a given folder. The file name is the md5 hash of the URL.

    Args:
        path (str): folder path
        url (str): URL of the file
        delay (float): delay
    """

    import requests
    from pathlib import Path
    import time

    try:
        hash_name = hash_str(url) + ".pdf"
        file_path = Path(path) / hash_name
        if file_path.exists():
            return False
        file_path.parent.mkdir(parents=True, exist_ok=True)
        time.sleep(delay)
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error with {url}: {e}")
        return False

def url_exists_in_file(url: str, file_name: str):
    """Check if the URL is already written in the file.
    """

    import os
    
    if not os.path.exists(file_name):
        return False
    with open(file_name, "r", encoding = "utf-8") as file:
        return any(line.strip() == url.strip() for line in file)

def store_url_corpus(url: str, file_name: str):
    """Stores URLs of PDFs to download.
    """
    if url_exists_in_file(url, file_name):
        print(f"{url} exists in {file_name}")
        return
    print("store:" ,file_name, url)
    with open(file_name, "a", encoding="utf-8") as archivo:
        archivo.write(url + "\n")

def read_urls_corpus(file_name: str) -> list[str]:
    try:
        with open(file_name, "r", encoding="utf-8") as archivo:
            # .strip() elimina el \n y espacios en blanco extra
            urls = [linea.strip() for linea in archivo if linea.strip()]
        return urls
    except FileNotFoundError:
        print("El archivo no existe todavía.")
        return []
    
def count_files(path: str):
    import os

    with os.scandir(path) as fs:
        return sum(1 for f in fs if f.is_file())
    
def time_since_creation_files(folder_path: str) -> list[tuple[str, float]]:
    """Time since the creation of the files on a folder.
    """

    import time
    import os
    from pathlib import Path

    folder = Path(folder_path)
    results = []
    now = time.time()
    for file in folder.iterdir():
        if file.is_file():
            file_time = os.path.getctime(file)
            results.append((file.name, now - file_time))
    results.sort(key = lambda x: x[1], reverse = True)
    return results

def delete_file(folder_path: str, file_name: str) -> bool:
    """Delete file_name at folder_path, returns if it was possible.
    """
    
    from pathlib import Path
    import os
    
    file_path = Path(folder_path) / file_name
    try:
        os.remove(file_path)
        return True
    except:
        return False