from indexing.index_bm25f import IndexBM25F
from utils.files import read_urls_corpus
from utils.hash import hash_str
from indexing.utils.document_parser import ExtractPdf
from utils.text_processor import chunking, TextPreprocessor
from indexing.dense_index import DenseIndexer
from indexing.persist_chunks import PersistChunk

def add2index(urls: list[str]):
    index_bm25f = IndexBM25F()
    dense_index = DenseIndexer()
    persist_chunks = PersistChunk()
    for i_, url in enumerate(urls):
        print(i_)
        url_hash = hash_str(url)
        pdf_path = "corpus/" + url_hash + ".pdf"
        ext_pdf = ExtractPdf(pdf_path)
        pdf_fields = ext_pdf.extract_pdf()
        text_processor = TextPreprocessor(pdf_fields['text'])
        clean_text = text_processor.get_clean_text()
        clean_tokens = clean_text.split()
        clean_chunks = chunking(clean_tokens)
        for (i, chunk) in enumerate(clean_chunks):
            chunk_hash = hash_str(url_hash + str(i))
            clean_chunk_text = " ".join(chunk)
            chunk_normalized_tokens = text_processor.get_normalized_tokens(clean_chunk_text)
            text_normalized = " ".join(chunk_normalized_tokens)
            index_bm25f.add_document({
                'id': chunk_hash,
                'title': pdf_fields['title'],
                'authors': pdf_fields['authors'],
                'abstract': pdf_fields['abstract'],
                'text': text_normalized,
                'pdf_hash': url_hash
            })
            dense_index.add_chunk({
                'text': clean_chunk_text,
                'pdf_hash': url_hash,
                'chunk_hash': chunk_hash
            })
            persist_chunks.persist_chunk({
                'chunk_hash': chunk_hash,
                'pdf_hash': url_hash,
                'title': pdf_fields['title'],
                'content': clean_chunk_text
            })
    dense_index.save()


def build_indexes():
    """Build BM25F and dense embeddings index.
    """

    corpus_urls_path = "downloaded_urls.txt"
    urls = read_urls_corpus(corpus_urls_path)
    add2index(urls)

# build_indexes()
# python3 -m indexing.build_indexes