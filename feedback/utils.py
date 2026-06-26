import PyPDF2


def extract_first_pages(doc_id: str, max_pages: int = 2) -> str:
    """Extract and return the text from the first two pages of a corpus PDF.

    Args:
        doc_id: The document identifier (filename without extension).

    Returns:
        Concatenated text from the first two pages. Returns an empty
        string if the file cannot be read or contains no extractable text.
    """

    path = doc_id
    try:
        with open(path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            pages = reader.pages[:max_pages]
            texts = [page.extract_text() or "" for page in pages]
            return "\n".join(texts).strip()
    except Exception:
        return ""
