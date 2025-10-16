from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="z-ai/glm-4.5-air:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "",  # Optional
        "X-Title": "",  # Optional
    }
)