from ranking.ranking import Ranker
from rag.ask_llm import ask_llm
from query_expansion.query_expander import PRFExpander

def retrieval_controller(query: str) -> list[str]:
    expander = PRFExpander()
    expanded_query = expander.expand(query)
    ranker = Ranker(query, expanded_query)
    pdfs = ranker.pdf_ranker()
    return ["corpus" + pdf + ".pdf" for pdf in pdfs]

def rag_controller(query: str) -> str:
    expander = PRFExpander()
    expanded_query = expander.expand(query)
    llm_answer = ask_llm(query, expanded_query)
    return llm_answer