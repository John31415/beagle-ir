import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.text_processor import TextPreprocessor

def _to_2d_float32(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype = np.float32)
    x = x.reshape(1, -1)
    return np.ascontiguousarray(x, dtype = np.float32)

def build_query_vector(query: str, vector = None) -> np.ndarray:
    if vector is not None:
        query_vector = _to_2d_float32(vector)
    else:
        tp = TextPreprocessor(query)
        tokens = tp.get_normalized_tokens()
        query_processed = " ".join(tokens)
        model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
        query_vector = model.encode([query_processed], convert_to_numpy = True, normalize_embeddings = False).astype(np.float32)
        query_vector = _to_2d_float32(query_vector)
    faiss.normalize_L2(query_vector)
    return query_vector