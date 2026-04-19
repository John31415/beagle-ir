from whoosh.index import open_dir
import os
from whoosh.qparser import MultifieldParser

def get_chunk_text(chunk_hash: str) -> str:
    """Returns the text of the chunk.
    """

    index_path = os.path.join("indexing", "index_dir")
    ix = open_dir(index_path)
    with ix.searcher() as searcher:
        qp = MultifieldParser(
            ["chunk_hash"],
            schema=ix.schema
        )
        q = qp.parse(chunk_hash)
        results = searcher.search(q, limit=1)
        return results[0]["content"]