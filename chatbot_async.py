from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import asyncio

load_dotenv()

llm = ChatOpenAI(
    model="mistralai/mistral-small-2603",
    base_url="https://api.xkiro.com/v1",
)

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform basic arithmetic operations on two numbers.
    Supported operations: add, sub, mul, div.
    """
    if operation == "add":
        result = first_num + second_num
    elif operation == "sub":
        result = first_num - second_num
    elif operation == "mul":
        result = first_num * second_num
    elif operation == "div":
        if second_num == 0:
            return {"error": "Can't divide by zero"}
        result = first_num / second_num
    else:
        return {"error": "Invalid operation"}

    return {"result": result}


tools = [calculator]
llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_graph():
    async def chat_node(state: ChatState):
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}


    tool_node = ToolNode(tools)

    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")

    chatbot = graph.compile()
    return chatbot

async def main():
    chatbot=build_graph()
    system_message = SystemMessage(
    content=(
        "You are a helpful AI assistant. "
        "Always answer only in English. "
        "Do not use any other language in your responses."
    )
    )
    output = await  chatbot.ainvoke({
        "messages": [
            system_message,
            HumanMessage(content="What is the sum of 100 and 200?")
        ]
    })

    print(output["messages"][-1].content)

if __name__=="__main__":
    asyncio.run(main())