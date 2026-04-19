from whoosh.index import open_dir
import os

def get_chunk_data(chunk_hash: str) -> dict:
    """Returns the text of the chunk.
    """

    index_path = os.path.join("indexing", "index_dir")
    ix = open_dir(index_path)
    with ix.searcher() as searcher:
        results = searcher.document(id = chunk_hash)
        return results