import math
from collections import defaultdict
from datetime import date
from utils.files import extracts_date_from_pdf


def get_doc_date(doc_id: str) -> date:
    try:
        day, month, year = extracts_date_from_pdf(f"corpus/{doc_id}.pdf")
        return date(day, month, year)
    except Exception:
        return date.today()


def rrf_fusion(
    lists: list[list[tuple[str, float]]], k=60, apply_date_penalty=False
) -> list[str]:
    scores = defaultdict(float)
    for current_list in lists:
        for rank, (doc_id, score) in enumerate(current_list):
            scores[doc_id] += (1.0 + math.log1p(max(0.0, score))) / (k + rank + 1)
    if apply_date_penalty:
        hoy = date.today()
        for doc_id in scores:
            date_doc = get_doc_date(doc_id)
            antique = max(0.0, (hoy - date_doc).days / 30.4375)
            penal_date = 1.0 / (1.0 + math.log2(1.0 + antique))
            scores[doc_id] *= penal_date
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, _ in ranked_docs]
