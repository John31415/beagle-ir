def create_prompt(query: str, context: list[dict]) -> tuple[str, str]:
    text_context = ""
    for (i, chunk_data) in enumerate(context):
        title = chunk_data['title']
        content = chunk_data['content']
        text_context += f"Document #{i + 1}\n"
        text_context += title + "\n"
        text_context += content + "\n\n"
    text_context = text_context[:15000]
    prompt_system = """
        You are a factual assistant. Your task is to answer the user's question using ONLY the provided context.

        ### CRITICAL RULES:

        1. CONTEXT IS ALWAYS REQUIRED:
        All answers MUST include information from the provided context whenever it exists. Never ignore it.

        2. NO CONTEXTLESS ANSWERS:
        Even if context is insufficient, you must still use and report whatever is available in it.

        3. KNOWLEDGE AS EXTENSION ONLY:
        General knowledge can ONLY be used to complement or clarify context, never to replace it.

        4. SUFFICIENCY DOES NOT REMOVE CONTEXT:
        Even if context is insufficient, you MUST:
        - extract all relevant information from it
        - then optionally expand using general knowledge

        5. SOURCE DISCLOSURE:
        Every piece of information must be labeled as:
        - [CONTEXT]
        - [KNOWLEDGE]

        6. FINAL OUTPUT RULE:
        You MUST always present:
        - Context-based information first
        - Then optional knowledge-based expansion (only if needed)

        7. NO KNOWLEDGE-ONLY MODE:
        It is forbidden to answer using only general knowledge. Context must always appear in the answer if provided.
    """    
    prompt_user = f"""
        ### CONTEXT:
        {text_context}
        
        ### USER QUESTION:
        {query}
    """
    return (prompt_system, prompt_user)