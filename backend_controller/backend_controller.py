from ranking.ranking import Ranker
from rag.ask_llm import ask_llm
from query_expansion.expand_query_dense import expand_query_dense
from recommender.recommender import recommender
from recommender.utils.persist_history import add_query
from datetime import datetime

def retrieval_controller(query: str) -> list[str]:
    cleaned_query = query.strip()
    if not cleaned_query:
        return []
    add_query(cleaned_query, datetime.now())
    expanded_query = expand_query_dense(query)
    ranker = Ranker(cleaned_query, expanded_query)
    pdfs = ranker.pdf_ranker()
    return ["corpus/" + pdf + ".pdf" for pdf in pdfs]

def rag_controller(query: str) -> str:
    cleaned_query = query.strip()
    if not cleaned_query:
        return ""
    add_query(cleaned_query, datetime.now())
    expanded_query = expand_query_dense(query)
    llm_answer = ask_llm(cleaned_query, expanded_query)
    return llm_answer

def get_recommendations() -> list[str]:
    pdfs = recommender()
    return ["corpus/" + pdf + ".pdf" for pdf in pdfs]