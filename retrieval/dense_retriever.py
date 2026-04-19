from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle
from utils.text_processor import TextPreprocessor 

def dense_retriever(query: str, top_n_chunks = 500) -> list[tuple[str, str]]:
    """Search chunks that semantically match the query

    Returns:
        list[str]: list of hashes of de PDF files, possibly repeated.
    """

    model_name = 'multi-qa-mpnet-base-dot-v1'
    save_dir = "indexing/dense_index"
    model = SentenceTransformer(model_name)
    index = faiss.read_index(os.path.join(save_dir, "vector_index.faiss"))
    metadata = None
    with open(os.path.join(save_dir, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    tp = TextPreprocessor(query)
    tokens = tp.get_normalized_tokens()
    query_processed = " ".join(tokens)
    query_vector = model.encode([query_processed], convert_to_numpy = True)
    faiss.normalize_L2(query_vector)
    D, I = index.search(query_vector.astype('float32'), top_n_chunks)
    ranking = [(metadata[idx]['chunk_hash'], metadata[idx]['pdf_hash']) for idx in I[0] if idx != -1]
    return ranking