from math import log2

def dedupe_preserve_order(items):
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def normalize_dict(scores: dict[str, float]) -> dict[str, float]:
    total = sum(scores.values())
    if total <= 0:
        return {}
    return {k: v / total for k, v in scores.items()}

def rank_weights(n: int) -> list[float]:
    """Descending weights
    """

    if n <= 0:
        return []
    raw = [1.0 / log2(r + 2.0) for r in range(n)]
    s = sum(raw)
    return [x / s for x in raw]