from indexing.index_bm25f import IndexBM25F
from utils.files import read_urls_corpus
from utils.hash import hash_str
from indexing.utils.document_parser import extract_pdf
from indexing.utils.text_processor import chunking, TextPreprocessor

def build_indexes():
    """Build BM25F index and (embeddings...)
    """

    corpus_urls_path = "downloaded_urls.txt"
    urls = read_urls_corpus(corpus_urls_path)
    index_bm25f = IndexBM25F()
    for i_, url in enumerate(urls):
        print(i_)
        url_hash = hash_str(url)
        pdf_path = "corpus/" + url_hash + ".pdf"
        pdf_fields = extract_pdf(pdf_path)
        text_processor = TextPreprocessor(pdf_fields['text'])
        tokens = text_processor.get_normalized_tokens()
        chunks = chunking(tokens)
        for (i, chunk) in enumerate(chunks):
            chunk_hash = hash_str(url_hash + str(i))
            chunk_fields = {
                'id': chunk_hash,
                'title': pdf_fields['title'],
                'authors': pdf_fields['authors'],
                'abstract': pdf_fields['abstract'],
                'text': " ".join(chunk),
                'pdf_hash': url_hash
            }
            index_bm25f.add_document(chunk_fields)

build_indexes()