from rag.generate_context import get_chunks_context
from rag.prompt import create_prompt
import os
from groq import Groq
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

def ask_llm(query: str, expanded_query: str) -> str:
    """Ask an LLM the user's query with the context retrieved by the system.
    """

    load_dotenv()
    context = get_chunks_context(query, expanded_query)
    prompt = create_prompt(query, context)
    try:
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = groq_client.chat.completions.create(
            model = "llama3-8b-8192",
            messages = [{"role": "user", "content": prompt}],
            max_completion_tokens = 512,
            temperature = 0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq failed with error: {e}.")
        hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))
        response = hf_client.chat.completions.create(
            model = "mistralai/Mistral-7B-Instruct-v0.3",
            messages = [{"role": "user", "content": prompt}],
            max_tokens = 512,
            temperature = 0.2,
        )
        return response.choices[0].message.content.strip()