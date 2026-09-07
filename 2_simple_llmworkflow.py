from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from typing import TypedDict

llm = ChatOllama(model="qwen3:4b")

# define state
class LLMState(TypedDict):
    topic:str
    outline:str
    blog:str

def llm_qa(state:LLMState)->LLMState:
    topic=state["topic"]
    prompt=f"create a detailed outline for a blog  around this tpoic: {topic}"
    answer=llm.invoke(prompt).content
    state['outline']=answer
    return state

def llm_blog(state:LLMState)->LLMState:
    outline=state["outline"]
    prompt=f"write a blog post through this outline:{outline}"
    answer=llm.invoke(prompt).content
    state['blog']=answer
    return state
# create graph
graph=StateGraph(LLMState)

# add node
graph.add_node("llm_qa",llm_qa)
graph.add_node("llm_blog",llm_blog)

# add edges

graph.add_edge(START,"llm_qa")
graph.add_edge("llm_qa","llm_blog")
graph.add_edge("llm_blog",END)

workflow=graph.compile()

initial_state={"topic":"plyometrices"}

final_state=workflow.invoke(initial_state)
print(final_state)