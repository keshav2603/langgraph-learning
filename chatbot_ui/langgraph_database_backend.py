from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

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

conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)
workflow=graph.compile(checkpointer=checkpointer)

config={"configurable":{"thread_id":"thread_2"}}

# responce=workflow.invoke(
#     {"messages":[HumanMessage(content="hi my name is ram")]},
#     config=config
# )

def retreve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
