import numpy as np
from ranking.ranking import Ranker
from query_expansion.utils.embeddings_utils import embed, normalize
from feedback.scoring import action_to_score
from feedback.utils import extract_first_pages
from feedback.rocchio import rocchio


def feedback_controller(
    feedback: tuple[str, list[tuple[str, str]]],
    alpha: float = 1.0,
    beta: float = 0.6,
    gamma: float = 0.6,
) -> list[str]:
    """Run the feedback refinement pipeline for every query in the input.

    Args:
        feedback: Mapping of query text to a list of (doc_id, action) pairs.
        alpha: Rocchio weight for the original query vector.
        beta: Rocchio weight for the positive centroid (relevant docs).
        gamma: Rocchio weight for the negative centroid (irrelevant docs).

    Returns:
        A dict mapping each query to a re-ranked list of doc_id strings.
    """

    query, doc_actions = feedback
    return _process_query(query, doc_actions, alpha, beta, gamma)


def _process_query(
    query: str,
    doc_actions: list[tuple[str, str]],
    alpha: float,
    beta: float,
    gamma: float,
) -> list[str] | None:
    """Refine a single query using its associated feedback signals.

    Args:
        query: The original query string.
        doc_actions: List of (doc_id, action) pairs for this query.
        alpha: Rocchio alpha (original query weight).
        beta: Rocchio beta (positive centroid weight).
        gamma: Rocchio gamma (negative centroid weight).

    Returns:
        Re-ranked list of doc_id strings from the retrieval module.
    """

    cleaned_query = query.strip()
    if not cleaned_query:
        return []
    q_vec = normalize(embed(query))
    scored_vecs = _build_scored_vecs(doc_actions)
    if not scored_vecs:
        return None
    q_refined = rocchio(q_vec, scored_vecs, alpha=alpha, beta=beta, gamma=gamma)
    ranker = Ranker(cleaned_query, q_refined)
    pdfs = ranker.pdf_ranker()
    return pdfs


def _build_scored_vecs(
    doc_actions: list[tuple[str, str]],
) -> list[tuple[np.ndarray, float]]:
    """Convert (doc_id, action) pairs to (embedding, score) pairs.

    Args:
        doc_actions: List of (doc_id, action) pairs.

    Returns:
        List of (embedding_vector, score) tuples ready for Rocchio.
    """

    scored_vecs: list[tuple[np.ndarray, float]] = []
    for doc_id, action in doc_actions:
        score = action_to_score(action)
        if score == 0.0:
            continue
        text = extract_first_pages(doc_id)
        if not text:
            continue
        doc_vec = normalize(embed(text))
        scored_vecs.append((doc_vec, score))
    return scored_vecs
