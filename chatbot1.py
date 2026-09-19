from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

load_dotenv()

llm = ChatOpenAI(
    model="mistralai/mistral-small-2603",
    base_url="https://api.xkiro.com/v1",
    api_key="sk-xt-6410a898be211b08ee4c267237ac4c7904059bd32d087020",
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


def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(tools)

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

workflow = graph.compile()


system_message = SystemMessage(
    content=(
        "You are a helpful AI assistant. "
        "Always answer only in English. "
        "Do not use any other language in your responses."
    )
)

out = workflow.invoke({
    "messages": [
        system_message,
        HumanMessage(content="What is the sum of 100 and 200? and also talk about the tool you used ")
    ]
})

print(out["messages"][-1].content)