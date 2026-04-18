def read_urls_corpus(file_name: str) -> list[str]:
    try:
        with open(file_name, "r", encoding="utf-8") as archivo:
            urls = [linea.strip() for linea in archivo if linea.strip()]
        return urls
    except FileNotFoundError:
        print("El archivo no existe todavía.")
        return []