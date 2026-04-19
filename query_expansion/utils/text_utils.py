from indexing.utils.document_parser import ExtractPdf
from utils.text_processor import TextPreprocessor

def get_text(pdf_hash: str) -> str:
    pdf_path = "corpus/" + pdf_hash + ".pdf"
    ext_pdf = ExtractPdf(pdf_path)
    pdf_fields = ext_pdf.extract_pdf()
    return pdf_fields["text"]

def clear_text(text: str) -> list[str]:
    tp = TextPreprocessor(text)
    tp.get_clean_text()
    tp.tokens = tp._tokenize()
    tp.tokens = tp._remove_stop_words()
    return tp.tokens