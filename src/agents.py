from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Essay Agent
def create_essay_agent():
    llm = ChatOpenAI(
        model="z-ai/glm-4.5-air:free",
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",  # Optional
        }
    )
    prompt = ChatPromptTemplate.from_template(
        "Write a comprehensive essay on the topic: {topic}. "
        "Make it well-structured with introduction, body, and conclusion. "
        "Current essay (if any): {current_essay}. "
        "Feedback: {feedback}"
    )
    return prompt | llm | StrOutputParser()

# Critique Agent
def create_critique_agent():
    llm = ChatOpenAI(
        model="z-ai/glm-4.5-air:free",
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",  # Optional
        }
    )
    prompt = ChatPromptTemplate.from_template(
        "Review the following essay on the topic: {topic}. "
        "Provide a rating out of 10 and suggest changes if needed. "
        "If the essay is good (rating 8+), say 'OK' to approve. "
        "Essay: {essay}"
    )
    return prompt | llm | StrOutputParser()