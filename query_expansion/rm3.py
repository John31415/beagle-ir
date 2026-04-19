from collections import Counter, defaultdict

def compute_term_probs(docs_tokens, doc_weights):
    """P(t | R) - the probability of a term given the (assumed) relevant documents.
    """

    term_probs = defaultdict(float)
    for i, tokens in enumerate(docs_tokens):
        weight = doc_weights[i]
        tf = Counter(tokens)
        doc_len = sum(tf.values())
        if doc_len == 0:
            continue
        for term, freq in tf.items():
            if len(term) < 2:
                continue
            term_probs[term] += (freq / doc_len) * weight
    return term_probs

def interpolate(query_tokens, term_probs, lambda_=0.35):
    """It combines the original query distribution P(t | q) and the expansion distribution P(t | R)
    """

    query_counter = Counter(query_tokens)
    total = sum(query_counter.values()) or 1
    query_probs = {t: c / total for t, c in query_counter.items()}
    final = defaultdict(float)
    for t, p in query_probs.items():
        final[t] += (1 - lambda_) * p
    for t, p in term_probs.items():
        final[t] += lambda_ * p
    return final