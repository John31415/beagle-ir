from collections import Counter
from datetime import datetime
from math import exp
import re
from recommender.utils.persist_history import get_all_queries

def build_historical_query(max_terms: int = 20, tau_days: float = 30.0) -> str:
    now = datetime.now()
    history = [(query.strip(), timestamp) for query, timestamp in get_all_queries() if query and query.strip()]
    if not history:
        return ""
    current_query = history[0][0]
    if not current_query:
        return ""
    term_weights = Counter()
    for query, ts in history:
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            dt = now
        age_days = max((now - dt).total_seconds() / 86400.0, 0.0)
        decay = exp(-age_days / tau_days)
        tokens = re.findall(r"[a-z0-9]+", query.lower())
        token_counts = Counter(t for t in tokens if len(t) >= 2)
        for term, count in token_counts.items():
            term_weights[term] += count * decay
    if not term_weights:
        return current_query
    ranked_terms = term_weights.most_common(max_terms)
    if len(ranked_terms) == 1:
        term, _ = ranked_terms[0]
        return " ".join([term] * 3)
    max_w = ranked_terms[0][1]
    min_w = ranked_terms[-1][1]
    denom = max(max_w - min_w, 1e-9)
    expanded_terms = []
    for term, weight in ranked_terms:
        norm = (weight - min_w) / denom
        repeats = 1 + round(2 * norm)
        repeats = max(1, min(3, repeats))
        expanded_terms.extend([term] * repeats)
    return " ".join(expanded_terms)