import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def normalize(v: np.ndarray, eps = 1e-12) -> np.ndarray:
    v = np.asarray(v, dtype = np.float32).reshape(-1)
    n = np.linalg.norm(v)
    if n < eps:
        return v
    return v / n

def embed(text: str) -> np.ndarray:
    """Text to normalize dense embedding.
    """

    if text is None:
        text = ""
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    vec = model.encode([text], convert_to_numpy = True, normalize_embeddings = False)[0]
    return normalize(vec)

def get_chunk_embedding(chunk_hash: str) -> np.ndarray:
    """Retrieve the embedding of a chunk from FAISS using reconstruct().
    """

    save_dir = "indexing/dense_index"
    index = faiss.read_index(os.path.join(save_dir, "vector_index.faiss"))
    metadata = None
    with open(os.path.join(save_dir, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    hash_to_pos = {v["chunk_hash"]: k for (k, v) in metadata.items()}
    pos = hash_to_pos[chunk_hash]
    vec = index.reconstruct(pos)
    return normalize(vec)