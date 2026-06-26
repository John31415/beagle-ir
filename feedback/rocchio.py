import numpy as np


def compute_centroid(
    vecs: list[np.ndarray],
    weights: list[float],
) -> np.ndarray | None:
    """Compute a weighted centroid from a list of vectors.

    Args:
        vecs: Non-empty list of 1-D numpy arrays of the same shape.
        weights: Parallel list of non-negative floats.

    Returns:
        A normalized 1-D numpy array, or None if `vecs` is empty.
    """

    if not vecs:
        return None
    stack = np.stack(vecs, axis=0).astype(np.float32)
    w = np.asarray(weights, dtype=np.float32)
    w_sum = float(w.sum())
    if w_sum <= 1e-12:
        centroid = np.mean(stack, axis=0)
    else:
        w = w / w_sum
        centroid = np.sum(stack * w[:, None], axis=0)
    return _normalize(centroid)


def rocchio(
    q_vec: np.ndarray,
    scored_vecs: list[tuple[np.ndarray, float]],
    alpha: float = 1.0,
    beta: float = 0.75,
    gamma: float = 0.25,
) -> np.ndarray:
    """Adjust a query vector using the Rocchio algorithm.

    Args:
        q_vec: Original query embedding.
        scored_vecs: List of (doc_embedding, score) pairs.
        alpha: Weight for the original query vector.
        beta: Weight for the positive centroid.
        gamma: Weight for the negative centroid.

    Returns:
        A normalized 1-D numpy array representing the refined query.
    """

    pos_vecs, pos_weights = [], []
    neg_vecs, neg_weights = [], []
    for vec, score in scored_vecs:
        if score > 0.0:
            pos_vecs.append(vec)
            pos_weights.append(score)
        elif score < 0.0:
            neg_vecs.append(vec)
            neg_weights.append(abs(score))
    q_new = alpha * q_vec.astype(np.float32)
    pos_centroid = compute_centroid(pos_vecs, pos_weights)
    if pos_centroid is not None:
        q_new = q_new + beta * pos_centroid
    neg_centroid = compute_centroid(neg_vecs, neg_weights)
    if neg_centroid is not None:
        q_new = q_new - gamma * neg_centroid
    return _normalize(q_new)


def _normalize(vec: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vec))
    if norm < 1e-12:
        return vec
    return vec / norm
