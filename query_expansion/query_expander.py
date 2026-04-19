from collections import defaultdict
from retrieval.bm25f_retriever import bm25f_retriever
from query_expansion.utils.text_utils import clear_text, get_text
from query_expansion.utils.math_utils import normalize_dict, rank_weights, dedupe_preserve_order
from query_expansion.rm3 import compute_term_probs, interpolate

class PRFExpander:
    """
    Example: \n
        expander = PRFExpander() \n
        expanded_query = expander.expand("neural ranking models")
    """

    def __init__(self, top_docs = 5, lambda_ = 0.35, top_terms = 20):
        self.top_docs = top_docs
        self.lambda_ = lambda_
        self.top_terms = top_terms

    def expand(self, query: str) -> str:
        query_tokens = clear_text(query)
        if not query_tokens:
            return query
        chunks = bm25f_retriever(query)
        if not chunks:
            return query
        pdf_hashes = [pdf for (_, pdf) in chunks]
        pdf_hashes = dedupe_preserve_order(pdf_hashes)[:self.top_docs]
        if not pdf_hashes:
            return query
        weights = rank_weights(len(pdf_hashes))
        docs_tokens = []
        for pdf_hash in pdf_hashes:
            text = get_text(pdf_hash)
            tokens = clear_text(text)
            docs_tokens.append(tokens)
        term_probs = compute_term_probs(docs_tokens, weights)
        term_probs = normalize_dict(term_probs)
        if not term_probs:
            return query
        final_scores = interpolate(query_tokens, term_probs, self.lambda_)
        return self._build_query(query_tokens, final_scores)

    def _build_query(self, query_tokens, scores):
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if not ranked:
            return " ".join(query_tokens)
        ranked = ranked[:self.top_terms]
        expanded = []
        original = set(query_tokens)
        max_score = ranked[0][1] if ranked[0][1] > 0 else 1.0
        for term, score in ranked:
            if term in original:
                repeats = 3
            else:
                repeats = max(1, min(3, int(round((score / max_score) * 3))))
            expanded.extend([term] * repeats)
        return " ".join(expanded)