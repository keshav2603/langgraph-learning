from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = PromptTemplate.from_template("""
You are a concise and direct AI assistant.

Rules:
- Answer the user's question directly.
- For simple factual questions, answer in 1-2 sentences.
- Do not give unnecessary explanations, disclaimers, or background information.
- Only provide detailed explanations when the user asks for them.
- Do not repeat the question.

Question: {question}
""")

model = ChatOllama(model="qwen3:4b")
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({
    "question": "What is the capital of India?"
})

print(result)