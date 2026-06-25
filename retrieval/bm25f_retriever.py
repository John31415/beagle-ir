from whoosh.index import open_dir
from whoosh.scoring import BM25F
import os
from utils.text_processor import TextPreprocessor
from whoosh.qparser import MultifieldParser, OrGroup

def bm25f_retriever(query: str, top_n_chunks = 100, relative_threshold = 0.9) -> list[tuple[str, str, int]]:
    """Search de top_n_chunks that satisfy the query

    Args:
        query (str): text query.
        top_n_chunks (int, optional): maximum number of chunks. Defaults to 100.
        relative_threshold (float, optional): fraction of the best score used. Defaults to 0.9.

    Returns:
        list[tuple[str, str]]: list of (chunk_hash, pdf_hash)
    """
    
    print("BM25F retriever")
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
        scored_hits = []
        for hit in results:
            chunk_hash = hit["id"]
            pdf_hash = hit["pdf_hash"]
            score = float(hit.score)
            scored_hits.append((chunk_hash, pdf_hash, score))
        if not scored_hits:
            return []
        score_threshold = scored_hits[0][2] * relative_threshold
        filtered = [(chunk_hash, pdf_hash, score) for (chunk_hash, pdf_hash, score) in scored_hits if score >= score_threshold]
        filtered.sort(key = lambda x: x[2], reverse = True)
    return filtered[:top_n_chunks]