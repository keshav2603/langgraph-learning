from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:4b")

print(llm.invoke("Hello").content)