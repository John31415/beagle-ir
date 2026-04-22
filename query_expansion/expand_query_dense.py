import numpy as np
from retrieval.dense_retriever import dense_retriever
from query_expansion.utils.embeddings_utils import embed, get_chunk_embedding, normalize

def expand_query_dense(query: str, k = 5, similarity_threshold = 0.70, alpha = 1.0, beta = 0.5) -> np.ndarray:
    """Expands the query into vector space. Returns a normalized embedding.
    """

    q_vec = embed(query)
    retrieved = dense_retriever(query, q_vec.reshape(1, -1), k)
    if not retrieved:
        return q_vec
    chunk_vecs = []
    sims = []
    for (chunk_hash, _) in retrieved:
        d_vec = get_chunk_embedding(chunk_hash)
        sim = float(np.dot(q_vec, d_vec))
        if sim >= similarity_threshold:
            chunk_vecs.append(d_vec)
            sims.append(sim)
    if not chunk_vecs:
        return q_vec
    weights = np.asarray(sims, dtype = np.float32)
    weights_sum = float(weights.sum())
    stack = np.stack(chunk_vecs, axis = 0)
    if weights_sum <= 1e-12:
        centroid = np.mean(stack, axis = 0)
    else:
        weights = weights / weights_sum
        centroid = np.sum(stack * weights[:, None], axis = 0)
    centroid = normalize(centroid)
    q_exp = alpha * q_vec + beta * centroid
    return normalize(q_exp)