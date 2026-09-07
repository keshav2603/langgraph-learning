from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOllama(model="qwen3:4b")

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]


def chat_node(state:ChatState):
    messages= state["messages"]


    response=llm.invoke(messages).content

    return {"messages":[AIMessage(response)]}
checkpointer=MemorySaver()
graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

workflow=graph.compile(checkpointer=checkpointer)

# print(workflow.invoke({"messages":[HumanMessage("hello how are you doing?")]})["messages"])
thread_id="1"
while True:
    user_message=input("type here :")
    print("User :",user_message)
    if(user_message.strip().lower() in ["exit","bye","quit"]):
        break;
    config={"configurable":{"thread_id":thread_id}}
    response=workflow.invoke({"messages":[HumanMessage(content=user_message)]},config=config)

    print("AI :",response["messages"][-1].content)