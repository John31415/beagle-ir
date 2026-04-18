import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class DenseIndexer:

    def __init__(self, model_name='multi-qa-mpnet-base-dot-v1'):
        self.save_dir = "indexing/dense_index"
        self.model = SentenceTransformer(model_name)
        self.dimension = 768
        self.index_path = os.path.join(self.save_dir, "vector_index.faiss")
        self.metadata_path = os.path.join(self.save_dir, "metadata.pkl")
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
            self.current_pos = len(self.metadata)
        else:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = {}
            self.current_pos = 0

    def add_chunk(self, chunk_data: dict):
        embedding = self.model.encode([chunk_data['text']], convert_to_numpy=True)
        faiss.normalize_L2(embedding)
        self.index.add(embedding.astype('float32'))
        self.metadata[self.current_pos] = {
            'chunk_hash': chunk_data['chunk_hash'],
            'pdf_hash': chunk_data['pdf_hash']
        }
        self.current_pos += 1

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)