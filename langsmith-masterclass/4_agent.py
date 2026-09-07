from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
# from langchain_classic.agents import AgentExecutor
# from langsmith import Client
from dotenv import load_dotenv
import requests
import os

os.environ["LANGCHAIN_PROJECT"]="sequential llm aap"

load_dotenv()

search_tool = DuckDuckGoSearchRun()

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=f07d9636974c4120025fadf60678771b&query={city}'

  response = requests.get(url)

  return response.json()


llm = ChatOllama(model="qwen3:4b")

# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_agent(
    model=llm,
    tools=[search_tool, get_weather_data],
)



# What is the release date of Dhadak 2?
# What is the current temp of gurgaon
# Identify the birthplace city of Kalpana Chawla (search) and give its current temperature.

# Step 5: Invoke
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Identify the birthplace city of Kalpana Chawla (search) and give its current temperature."
            }
        ]
    }
)


print(response)

# print(response['output'])