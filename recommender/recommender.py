from recommender.build_historical_query import build_historical_query
from ranking.ranking import Ranker

def recommender() -> list[str]:
    query = build_historical_query()
    ranker = Ranker(query)
    pdfs = ranker.pdf_ranker()
    return pdfs