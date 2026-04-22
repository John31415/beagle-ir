import faiss
import os
import pickle
from retrieval.utils.dense_utils import build_query_vector

def dense_retriever(query: str, vector = None, top_n_chunks = 100, chunk_similarity_threshold = 0.5) -> list[tuple[str, str]]:
    """Search chunks that semantically match the query

    Returns:
        list[str]: list of (chunk_hash, pdf_hash)
    """

    save_dir = "indexing/dense_index"
    index = faiss.read_index(os.path.join(save_dir, "vector_index.faiss"))
    metadata = None
    with open(os.path.join(save_dir, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    query_vector = build_query_vector(query, vector)
    D, I = index.search(query_vector, top_n_chunks)
    chunk_candidates= []
    for score, idx in zip(D[0], I[0]):
        if idx != -1 and float(score) >= chunk_similarity_threshold:
            chunk_candidates.append((metadata[idx]["chunk_hash"], metadata[idx]["pdf_hash"], score))
    filtered = [(chunk_hash, pdf_hash, score) for (chunk_hash, pdf_hash, score) in chunk_candidates]
    filtered.sort(key = lambda x: x[2], reverse = True)
    return [(chunk_hash, pdf_hash) for (chunk_hash, pdf_hash, _) in filtered[:top_n_chunks]]