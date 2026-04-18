from collections import defaultdict

def rrf_fusion(list_bm25: list[str], list_dense: list[str], k = 60) -> list[str]:
    """Reciprocal Rank Funsion for combining search results
    """

    scores = defaultdict(float)
    for rank, doc_id in enumerate(list_bm25):
        scores[doc_id] += 1.0 / (k + rank + 1)
    for rank, doc_id in enumerate(list_dense):
        scores[doc_id] += 1.0 / (k + rank + 1)
    ranked_docs = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    return [doc_id for doc_id, _ in ranked_docs]