from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal


class QuadState(TypedDict):
    a:int
    b:int
    c:int
    equation:str
    discriminant:float
    result:str

def show_equation(state:QuadState)->QuadState:
    equation=f"{state["a"]}x^2 {state["b"]}x {state['c']}"

    return {"equation":equation}

def calculate_discriminant(state:QuadState)->QuadState:
    d=(state["b"]*state["b"])-4*state["a"]*state["c"]

    return {"discriminant":d}

def real_root(state:QuadState)->QuadState:
    root1= (-state["b"]+state["discriminant"]**2)/(state["a"]*2)
    root2= (-state["b"]-state["discriminant"]**2)/(state["a"]*2)

    result=f"the roots are {root1} and {root2}"
    return{"result":result}

def repeated_root(state:QuadState)->QuadState:
    root1=(-state["b"])/(state["a"]*2)

    result = f"only repeating roots is {root1}"
    return {"result":result}

def no_real_root(state:QuadState)->QuadState:
    return {"result":"no real roots exist"}

def check_condition(state:QuadState)->Literal["repeated_root","real_root","no_real_root"]:

    if(state["discriminant"]==0):
        return "repeated_root"
    elif(state["discriminant"]>0):
        return "real_root"
    else:
        return "no_real_root"


graph=StateGraph(QuadState)

graph.add_node("show_equation",show_equation)
graph.add_node("calculate_discriminant",calculate_discriminant)
graph.add_node("real_root",real_root)
graph.add_node("repeated_root",repeated_root)
graph.add_node("no_real_root",no_real_root)

graph.add_edge(START,"show_equation")
graph.add_edge("show_equation","calculate_discriminant")
graph.add_conditional_edges("calculate_discriminant",check_condition)
graph.add_edge("real_root",END)
graph.add_edge("repeated_root",END)
graph.add_edge("no_real_root",END)


workflow=graph.compile()

initial_state={"a":1,"b":2,"c":3}
output=workflow.invoke(initial_state)
print(output)