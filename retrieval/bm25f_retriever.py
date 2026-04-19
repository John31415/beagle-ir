from whoosh.index import open_dir
from whoosh.scoring import BM25F
import os
from utils.text_processor import TextPreprocessor
from whoosh.qparser import MultifieldParser, OrGroup

def bm25f_retriever(query: str, top_n_chunks = 500) -> list[tuple[str, str]]:
    """Search de top_n_chunks that satisfy the query

    Args:
        query (str): text query.
        top_n_chunks (int, optional): maximum number of chunks. Defaults to 500.

    Returns:
        list[tuple[str, str]]: list of (chunk_hash, pdf_hash)
    """
    
    tp = TextPreprocessor(query)
    tokens_query = tp.get_normalized_tokens()
    clean_query = " ".join(tokens_query)
    index_path = os.path.join("indexing", "index_dir")
    ix = open_dir(index_path)
    with ix.searcher(weighting = BM25F(k1=1.7, b=0.65)) as searcher:
        parser = MultifieldParser(
            ["title", "abstract", "content"], 
            ix.schema, 
            group = OrGroup.factory(0.7)
        )
        q = parser.parse(clean_query)
        results = searcher.search(q, limit = top_n_chunks)
        pdf_hashes = [(hit['id'], hit['pdf_hash']) for hit in results]
    return pdf_hashes