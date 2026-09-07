from langgraph.graph import StateGraph,START,END
from langchain_ollama import ChatOllama
from typing import TypedDict, Literal
from pydantic import BaseModel,Field

llm = ChatOllama(model="qwen3:4b")


class SentimentSchema(BaseModel):
    sentiment:Literal["positive","negative"]=Field(description="sentiment of the review")

struct_llm=llm.with_structured_output(SentimentSchema)

class DiagnosisSchema(BaseModel):
    issue_type:Literal["UX","performance","bug","support","other"]=Field(description="the category of the issue according to the review")
    tone:Literal["angry","disppointed","calm","frustrated"]=Field(description="the emotional tone used by the user")
    urgency:Literal["low","medium","high"]=Field(description="urgency fo the issue appear ot be")

diagnosis_llm=llm.with_structured_output(DiagnosisSchema)


class ReviewState(TypedDict):
    review:str
    sentiment:Literal["positive","negative"]
    diagnosis:dict
    response:str

def find_sentiment(state:ReviewState)->Literal["positive","negative"]:
    prompt=f"find the sentiment of the following review --\n{state['review']}"
    output=struct_llm.invoke(prompt).sentiment
    return {"sentiment":output}

def check_sentiment(state:ReviewState)->Literal["positive_response","run_diagnosis"]:
    return "run_diagnosis" if state["sentiment"]=="negative" else "positive_response"

def positive_response(state:ReviewState)->ReviewState:
    prompt=f"""Write a warm thank-you message in responce to this review\n\n{state['review']}\n\nalso ask user to give a feedback on our website kindly"""
    response=llm.invoke(prompt).content
    return {"response":response}

def run_diagnosis(state:ReviewState)->ReviewState:
    prompt=f"diagnose this negative review \n\n {state['review']}\n\n return the issue type,tone,urgency"
    output=diagnosis_llm.invoke(prompt)
    return {"diagnosis":output.model_dump()}

def negative_response(state:ReviewState)->ReviewState:
    prompt=f"""
    you are a support assistant,
    the user had a issue {state['diagnosis']['issue_type']}sounded {state['diagnosis']['tone']}
    and marked urgency is {state['diagnosis']['urgency']}
    write a empathetic, helpful resolution message
"""
    output=llm.invoke(prompt).content
    return {"response":output}

graph=StateGraph(ReviewState)

graph.add_node("find_sentiment",find_sentiment)
graph.add_node("positive_response",positive_response)
graph.add_node("negative_response",negative_response)
graph.add_node("run_diagnosis",run_diagnosis)

graph.add_edge(START,"find_sentiment")
graph.add_conditional_edges("find_sentiment",check_sentiment)
graph.add_edge("positive_response",END)
graph.add_edge("run_diagnosis","negative_response")
graph.add_edge("negative_response",END) 


workflow=graph.compile()
intial_state={"review":"this product is bad the perfornmance it give is bad like and if you run anythign heavy it get hot "}
output=workflow.invoke(intial_state)

print(output)

# print(struct_llm.invoke("i don't like this phone battery is okey and display size is good but performance is really bad"))