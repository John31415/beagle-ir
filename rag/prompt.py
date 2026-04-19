def create_prompt(query: str, context: list[dict]) -> str:
    text_context = ""
    for (i, chunk_data) in enumerate(context):
        title = chunk_data['title']
        content = chunk_data['content']
        text_context += f"Document #{i + 1}\n"
        text_context += title + "\n"
        text_context += content + "\n\n"

    prompt = f"""
        You are a factual assistant. Your task is to answer the user's question using ONLY the provided context.

        ### CONTEXT:
        {text_context}
        
        ### USER QUESTION:
        {query}
        
        ### CRITICAL RULES:
        1. ANALYSIS: Evaluate if the CONTEXT provided above contains enough specific information to answer the question completely.
        2. LIMITATION: If the context is insufficient, missing details, or irrelevant to the question, respond EXACTLY with: "I'm sorry, but the provided documentation does not contain enough information to answer this question."
        3. NO OUTSIDE KNOWLEDGE: Do not use any internal knowledge or facts not present in the text above. 
        4. ACCURACY: If the information is sufficient, provide a direct and concise answer based strictly on the text.
    """

    return prompt