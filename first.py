# from langchain_ollama import ChatOllama

# llm = ChatOllama(model="qwen3:4b")

# print(llm.invoke("Hello").content)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="mistralai/mistral-small-2603",
    base_url="https://api.xkiro.com/v1",
    api_key="sk-xt-6410a898be211b08ee4c267237ac4c7904059bd32d087020",
)

response = llm.invoke([
    (
        "system",
        "You are a helpful AI assistant. Always respond in English."
    ),
    (
        "human",
        "What is LangGraph?"
    )
])

print(response.content)