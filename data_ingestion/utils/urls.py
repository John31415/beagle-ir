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
    from utils.hash import hash_str

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