from recommender.build_historical_query import build_historical_query
from query_expansion.query_expander import PRFExpander
from ranking.ranking import Ranker

def recommender() -> list[str]:
    query = build_historical_query()
    if not query:
        return []
    expander = PRFExpander()
    expanded_query = expander.expand(query)
    ranker = Ranker(query, expanded_query)
    pdfs = ranker.pdf_ranker()
    return pdfs