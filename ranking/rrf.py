from collections import defaultdict

def rrf_fusion(lists: list[list[str]], k = 60) -> list[str]:
    """Reciprocal Rank Funsion for combining search results
    """

    scores = defaultdict(float)
    for i in range(len(lists)):
        for rank, doc_id in enumerate(lists[i]):
            scores[doc_id] += 1.0 / (k + rank + 1)
    ranked_docs = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    return [doc_id for doc_id, _ in ranked_docs]