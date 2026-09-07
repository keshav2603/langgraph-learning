from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from langgraph.checkpoint.memory import InMemorySaver

llm = ChatOllama(model="qwen3:4b")
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

def chat_node(state:chat_node):
    messages=state["messages"]
    responce=llm.invoke(messages).content
    return {"messages":[AIMessage(responce)]}

graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)



checkpointer=InMemorySaver()
workflow=graph.compile(checkpointer=checkpointer)



