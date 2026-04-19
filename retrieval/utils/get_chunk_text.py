from whoosh.index import open_dir
import os

def get_chunk_text(chunk_hash: str) -> str:
    """Returns the text of the chunk.
    """

    index_path = os.path.join("indexing", "index_dir")
    ix = open_dir(index_path)
    with ix.searcher() as searcher:
        results = searcher.document(id = chunk_hash)
        print(results)
        return results["content"]