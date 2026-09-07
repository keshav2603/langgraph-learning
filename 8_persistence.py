from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict

llm = ChatOllama(model="qwen3:4b")


class JokeState(TypedDict):
    topic:str
    joke:str
    explanation:str

def gen_joke(state:JokeState)->dict:
    prompt = f"generate a hilarious joke on the topic:\n\n{state['topic']}\n\nunder 30 characters"

    response=llm.invoke(prompt).content
    return {"joke":response}

def exp_joke(state:JokeState)->dict:
    prompt=f"generate the explanation of the joke :\n\n{state['joke']}\n\n under 100 character"
    response=llm.invoke(prompt).content
    return {"explanation":response}

graph=StateGraph(JokeState)

graph.add_node("gen_joke",gen_joke)
graph.add_node("exp_joke",exp_joke)

graph.add_edge(START,"gen_joke")
graph.add_edge("gen_joke","exp_joke")
graph.add_edge("exp_joke",END)

# checkpointer

checkpointer= InMemorySaver()



workflow=graph.compile(checkpointer=checkpointer)

# we need to send a thread id so while using presistance so that we can access the saved state for that respective thread id 
config={"configurable":{"thread_id":"1"}}

workflow.invoke({"topic":"coding"},config=config)


workflow.get_state(config) #this give us the final state after the exicution

workflow.get_state_history(config) # this give use the value of state at every checkpoint(i.e after every superstep)


# how this will work on fault tolerance 

# if let's say our workflow break at generation explanation so we can do like 

workflow.invoke(None,config=config)

# if we do the our workflow will not start from the very start it will start from the gen explantion 


# time travel basically rerunning the workflwo from desired checkpoint 

workflow.invoke(None,config={"configurable":{"thread_id":"1","checkpoint_id":"13i193ij3ur2i31"}})

# we can also updated state at our desired checkpoint

workflow.update_state({"configurable":{"thread_id":"1","checkpoint_id":"13i193ij3ur2i31"}},{"topic":"somasa"})