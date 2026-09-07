from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from typing import TypedDict

llm = ChatOllama(model="qwen3:4b")


class Batsman(TypedDict):
    balls:int
    runs:int
    fours:int
    sixes:int

    sr:float
    bpb:float
    brp:float

def calc_sr(state:Batsman)->Batsman:
    sr=round((state["runs"]/state["balls"])*100,2)
    return {"sr":sr}

def calc_bpb(state:Batsman)->Batsman:
    bpb=round((state["balls"]/(state["fours"]+state["sixes"])),2)
    return {"bpb":bpb}

def calc_brp(state:Batsman)->Batsman:
   brp=round(((state["fours"]*4+state["sixes"]*6)/state["runs"])*100,2)
   return {"brp":brp}
def summary(state:Batsman)->Batsman:
    print("total runs:",state["runs"])
    print("total balls:",state["balls"])
    print("total fours:",state["fours"])
    print("total sixes:",state["sixes"])
    print("total strike rate:",state["sr"])
    print("ball per boundary:",state["bpb"])
    print("boundary percentage:",state["brp"])

graph=StateGraph(Batsman)

graph.add_node("calc_sr",calc_sr)
graph.add_node("calc_bpb",calc_bpb)
graph.add_node("calc_brp",calc_brp)
graph.add_node("summary",summary)


graph.add_edge(START,"calc_sr")
graph.add_edge(START,"calc_bpb")
graph.add_edge(START,"calc_brp")
graph.add_edge("calc_sr","summary")
graph.add_edge("calc_sr","summary")
graph.add_edge("calc_sr","summary")
graph.add_edge("summary",END)

work_flow=graph.compile()

output=work_flow.invoke({"balls":10,"fours":2,"sixes":1,"runs":20})
print(output)