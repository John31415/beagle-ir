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
    
def match_url2pdf(folder_path: str, urls_file_path: str, store_path: str):
    """Match URLs and PDF files downlaoded, then stores the list of URLs matched.
    """

    from utils.hash import hash_str
    import os

    urls = []
    with open(urls_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url:
                urls.append(url)
    hash_to_url = {}
    for url in urls:
        h = hash_str(url)
        hash_to_url[h] = url
    matched_urls = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_hash = filename[:-4]
            if file_hash in hash_to_url:
                matched_urls.append(hash_to_url[file_hash])
            else:
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
    with open(store_path, 'w', encoding='utf-8') as f:
        for url in matched_urls:
            f.write(url + '\n')

match_url2pdf("corpus", "corpus_urls.txt", "downloaded_urls.txt")