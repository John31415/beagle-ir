from ranking.ranking import Ranker
from rag.ask_llm import ask_llm
from query_expansion.query_expander import PRFExpander
from recommender.recommender import recommender
from recommender.utils.persist_history import add_query
from datetime import datetime

def retrieval_controller(query: str) -> list[str]:
    cleaned_query = query.strip()
    if not cleaned_query:
        return []
    add_query(cleaned_query, datetime.now())
    expander = PRFExpander()
    expanded_query = expander.expand(cleaned_query)
    ranker = Ranker(cleaned_query, expanded_query)
    pdfs = ranker.pdf_ranker()
    return ["corpus/" + pdf + ".pdf" for pdf in pdfs]

def rag_controller(query: str) -> str:
    cleaned_query = query.strip()
    if not cleaned_query:
        return ""
    add_query(cleaned_query, datetime.now())
    expander = PRFExpander()
    expanded_query = expander.expand(cleaned_query)
    llm_answer = ask_llm(cleaned_query, expanded_query)
    return llm_answer

def get_recommendations() -> list[str]:
    pdfs = recommender()
    return ["corpus/" + pdf + ".pdf" for pdf in pdfs]