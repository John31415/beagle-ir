from retrieval.bm25f_retriever import bm25f_retriever
from retrieval.dense_retriever import dense_retriever
from ranking.rrf import rrf_fusion

class Ranker:
    """Rank PDF files or chunks matching a query.
    """

    def __init__(self, query: str):
        self.query = query
        self.chunk2pdf = {}

    def chunk_ranker(self) -> list[str]:
        bm25f_match = bm25f_retriever(self.query)
        bm25f_chunks = []
        for (chunk, pdf) in bm25f_match:
            self.chunk2pdf[chunk] = pdf
            bm25f_chunks.append(chunk)
        dense_match = dense_retriever(self.query)
        dense_chunks = []
        for (chunk, pdf) in dense_match:
            self.chunk2pdf[chunk] = pdf
            dense_chunks.append(chunk)
        rrf_match = rrf_fusion([bm25f_chunks, dense_chunks])
        return rrf_match
    
    def pdf_ranker(self) -> list[str]:
        s = set()
        rank = []
        chunk_rank = self.chunk_ranker()
        for chunk in chunk_rank:
            pdf = self.chunk2pdf[chunk]
            if pdf not in s:
                rank.append(pdf)
                s.add(pdf)
        return rank