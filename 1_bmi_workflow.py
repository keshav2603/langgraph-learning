from langgraph.graph import StateGraph,START,END
from typing import TypedDict

# define state
class BMIState(TypedDict):
    weight_kg:float
    height_m:float
    bmi:float

# defining node function
def calculate_bmi(state:BMIState)->BMIState:
    weight=state["weight_kg"]
    height=state['height_m']
    bmi=weight/(height**2)
    state["bmi"]=round(bmi,2)

    return state


# define graph
graph=StateGraph(BMIState)

# add nodes to graph
graph.add_node("calculate_bmi",calculate_bmi)

# add edges to the graph
graph.add_edge(START,"calculate_bmi")
graph.add_edge("calculate_bmi",END)   

#compine the graph
workflow=graph.compile()

#exicute the graph

initial_state={"weight_kg":80,"height_m":1.73}
final_state=workflow.invoke(initial_state)
print(final_state)