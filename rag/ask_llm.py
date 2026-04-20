from rag.generate_context import get_chunks_context
from rag.prompt import create_prompt
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from pathlib import Path

def ask_llm(query: str, expanded_query: str) -> str:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path = env_path)
    context = get_chunks_context(query, expanded_query)
    prompt = create_prompt(query, context)
    client = InferenceClient(model = "Qwen/Qwen2.5-7B-Instruct", token = os.getenv("HF_TOKEN"))
    try:
        response = client.chat_completion(
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens = 512,
            temperature = 0.2,
        )
        return response.choices[0].message.content.strip()
    except:
        return "The system is experiencing some problems, please try again later"
    
print(ask_llm("what is quantum mechanics", "quantum quantum quantum mechanics mechanics mechanics physics"))