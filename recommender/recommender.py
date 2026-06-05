from recommender.build_historical_query import build_historical_query
from query_expansion.expand_query_dense import expand_query_dense
from ranking.ranking import Ranker

def recommender() -> list[str]:
    print("Recommender activated")
    query = build_historical_query()
    if not query:
        return []
    expanded_query = expand_query_dense(query)
    ranker = Ranker(query, expanded_query)
    pdfs = ranker.pdf_ranker(active_web_search = False)
    return pdfs