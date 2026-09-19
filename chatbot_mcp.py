from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

llm = ChatOpenAI(
    model="mistralai/mistral-small-2603",
    base_url="https://api.xkiro.com/v1",
)
client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": "/opt/homebrew/bin/uv",
            "args": [
                "run",
                "--directory",
                "/Users/keshavmacbook/Projects/AI-ML/fastmcp-demo-server",
                "server.py"
            ]
        }
    }
)




class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def build_graph():

    tools=await client.get_tools()
    print(tools)
    llm_with_tools=llm.bind_tools(tools)
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
    chatbot=await build_graph()
    system_message = SystemMessage(
    content=(
        "You are a helpful AI assistant. "
        "Always answer only in English. "
        "Do not use any other language in your responses."
    )
    )
    output = await chatbot.ainvoke({
        "messages": [
            system_message,
            HumanMessage(content="find the modulus of 13 and 23 and answer like a cricket commentator")
        ]
    })

    print(output["messages"][-1].content)

if __name__=="__main__":
    asyncio.run(main())