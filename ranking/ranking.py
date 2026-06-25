from retrieval.bm25f_retriever import bm25f_retriever
from retrieval.dense_retriever import dense_retriever
from ranking.rrf import rrf_fusion
from web_search.web_search import web_search
from collections import defaultdict


class Ranker:
    """Rank PDF files or chunks matching a query."""

    def __init__(self, query: str, expanded_query):
        self.query = query
        self.expanded_query = expanded_query
        self.chunk2pdf = {}

    def chunk_ranker(self) -> list[tuple[str, float]]:
        chunk2score = defaultdict(float)
        bm25f_match = bm25f_retriever(self.query)
        bm25f_chunks = []
        for chunk, pdf, score in bm25f_match:
            self.chunk2pdf[chunk] = pdf
            bm25f_chunks.append((chunk, score))
            chunk2score[chunk] = max(chunk2score[chunk], score)
        dense_match = dense_retriever(self.query, self.expanded_query)
        dense_chunks = []
        for chunk, pdf, score in dense_match:
            self.chunk2pdf[chunk] = pdf
            dense_chunks.append((chunk, score))
            chunk2score[chunk] = max(chunk2score[chunk], score)
        rrf_match = rrf_fusion([bm25f_chunks, dense_chunks], apply_date_penalty=False)
        return [(d, chunk2score[d]) for d in rrf_match]

    def pdf_ranker(self, rank_limit=20, active_web_search=True) -> list[str]:
        s = set()
        rank = []
        pdf2score = defaultdict(float)
        chunk_rank = self.chunk_ranker()
        for chunk, score in chunk_rank:
            pdf = self.chunk2pdf[chunk]
            pdf2score[pdf] = max(pdf2score[pdf], score)
            if pdf not in s:
                rank.append(pdf)
                s.add(pdf)
        if len(rank) < rank_limit:
            rank_with_scores = [(d, pdf2score[d]) for d in rank]
            web_pdfs = (
                web_search(self.query, min(3, rank_limit - len(rank)))
                if active_web_search
                else []
            )
            web_pdfs_with_scores = [(i, 0.0) for i in web_pdfs]
            rank = rrf_fusion(
                [rank_with_scores, web_pdfs_with_scores], apply_date_penalty=True
            )
        return rank[:rank_limit]
