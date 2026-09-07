from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ["LANGCHAIN_PROJECT"]="sequential llm aap"

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatOllama(model="qwen3:4b")

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

config={
    'run_name':"sequential_chain",
    "tags":["llm app","sequential work flow"],
    "metadata":{"model1":"qwen3:4b"}
}

result = chain.invoke({'topic': 'Unemployment in India'})

print(result)
