import re
from PyPDF2 import PdfReader


def read_urls_corpus(file_name: str) -> list[str]:
    try:
        with open(file_name, "r", encoding="utf-8") as archivo:
            urls = [linea.strip() for linea in archivo if linea.strip()]
        return urls
    except FileNotFoundError:
        print("El archivo no existe todavía.")
        return []


def extracts_date_from_pdf(pdf_path: str) -> tuple[int, int, int]:
    """Extracts date 'arXiv:YYMM.NNNNNvN [...] DD Mmm YYYY'."""

    month2num = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    try:
        reader = PdfReader(pdf_path)
        first_page = reader.pages[0].extract_text()
        pattern = r"arXiv:\d{4}\.\d{4,5}(?:v\d+)?\s+\[[^\]]+\]\s+(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})"
        match = re.search(pattern, first_page)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            month_num = month2num.get(month, month)
            return (day, month_num, year)
    except Exception as e:
        print(f"Error processing PDF: {e}")
    return (1, 1, 1)
