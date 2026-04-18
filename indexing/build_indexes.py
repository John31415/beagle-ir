from indexing.index_bm25f import IndexBM25F
from utils.files import read_urls_corpus
from utils.hash import hash_str
from utils.document_parser import ExtractPdf
from utils.text_processor import chunking, TextPreprocessor
from indexing.dense_index import DenseIndexer

def build_indexes():
    """Build BM25F index and (embeddings...)
    """

    corpus_urls_path = "downloaded_urls.txt"
    urls = read_urls_corpus(corpus_urls_path)
    index_bm25f = IndexBM25F()
    dense_index = DenseIndexer()
    for i_, url in enumerate(urls):
        print(i_)
        url_hash = hash_str(url)
        pdf_path = "corpus/" + url_hash + ".pdf"
        ext_pdf = ExtractPdf(pdf_path)
        pdf_fields = ext_pdf.extract_pdf()
        text_processor = TextPreprocessor(pdf_fields['text'])
        tokens = text_processor.get_normalized_tokens()
        chunks = chunking(tokens)
        for (i, chunk) in enumerate(chunks):
            chunk_hash = hash_str(url_hash + str(i))
            text = " ".join(chunk)
            index_bm25f.add_document({
                'id': chunk_hash,
                'title': pdf_fields['title'],
                'authors': pdf_fields['authors'],
                'abstract': pdf_fields['abstract'],
                'text': text,
                'pdf_hash': url_hash
            })
            dense_index.add_chunk({
                'text': text,
                'pdf_hash': url_hash,
                'chunk_hash': chunk_hash
            })
    dense_index.save()

build_indexes()