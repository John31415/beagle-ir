from ranking.ranking import Ranker
from indexing.persist_chunks import PersistChunk


def get_chunks_context(
    query: str, expanded_query: str, top_k_docs: int = 10
) -> list[dict]:
    ranker = Ranker(query, expanded_query)
    chunks_rank = ranker.chunk_ranker()[:top_k_docs]
    context = []
    persist_chunk = PersistChunk()
    for chunk, _ in chunks_rank:
        chunk_data = persist_chunk.get_chunk_by_hash(chunk)
        context.append(
            {
                "title": chunk_data["title"],
                "content": chunk_data["content"],
                "pdf_hash": chunk_data["pdf_hash"],
            }
        )
    return context
