from ranking.ranking import Ranker
from indexing.persist_chunks import PersistChunk

def get_chunks_context(query: str, expanded_query: str) -> list[dict]:
    ranker = Ranker(query, expanded_query)
    chunks_rank = ranker.chunk_ranker()
    context = []
    persist_chunk = PersistChunk()
    for chunk in chunks_rank:
        chunk_data = persist_chunk.get_chunk_by_hash(chunk)
        context.append({
            'title': chunk_data['title'],
            'content': chunk_data['content']
        })
    return context