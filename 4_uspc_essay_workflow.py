from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
import operator

llm = ChatOllama(model="qwen3:4b")


class EvaluationSchema(BaseModel):
    feedback:str=Field(description="detailed feedback for this motivational line")
    score:int=Field(description="score this motivational line out of 10",gt=0,le=10)


structured_model=llm.with_structured_output(EvaluationSchema)

# essay="""

# """

# output=structured_model.invoke(essay)
# print(output)

class LineState(TypedDict):
    m_line:str
    m_level_feedback:str
    depth_feedback:str
    overall_feedback:str
    ind_score:Annotated[list[int],operator.add]
    avg_score:float

def motivation_feedback(state:LineState)->LineState:
    prompt=f"give a detailed feedback and score on the line :{state['m_line']} based on the level of motivation it give"
    output=structured_model.invoke(prompt)
    return {"m_level_feedback":output.feedback,"ind_score":[output.score]}


def depth_level_feedback(state:LineState)->LineState:
    prompt=f"give a detailed feedback and score on the line :{state['m_line']} based on the level of depth it contain"
    output=structured_model.invoke(prompt)
    return {"depth_feedback":output.feedback,"ind_score":[output.score]}

def final_feedback(state:LineState)->LineState:
    prompt=f"give a detailed feedback on a motivational line based on the motivation level feedback:{state['m_level_feedback']} and the depth of the line feedback:{state["depth_feedback"]}"
    output=llm.invoke(prompt).content
    avg_score=sum(state["ind_score"])/len(state["ind_score"])
    return {"overall_feedback":output,"avg_score":avg_score}

graph=StateGraph(LineState)

graph.add_node("motivation_feedback",motivation_feedback)
graph.add_node("depth_level_feedback",depth_level_feedback)
graph.add_node("final_feedback",final_feedback)


graph.add_edge(START,"motivation_feedback")
graph.add_edge(START,"depth_level_feedback")
graph.add_edge("motivation_feedback","final_feedback")
graph.add_edge("motivation_feedback","final_feedback")
graph.add_edge("final_feedback",END)

workflow=graph.compile()
workflow.invoke({"m_line":"the more you sweat while train less you blead in war"})