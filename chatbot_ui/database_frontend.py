import streamlit as st

from langchain_core.messages import HumanMessage
from langgraph_database_backend import retreve_all_threads,workflow
import uuid
from dotenv import load_dotenv
load_dotenv()

# utils ************************************?***********
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state["thread_id"]=thread_id
    add_thread(thread_id)
    st.session_state["message_history"]=[]
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state["chat_threads"].append(thread_id)
def load_conversation(thread_id):
    return workflow.get_state(config={"configurable":{"thread_id":thread_id}}).values["messages"]

# session setup ****************************************

if "message_history" not in st.session_state:
    st.session_state["message_history"]=[]

if "thread_id" not in st.session_state:
    st.session_state["thread_id"]= generate_thread_id()
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"]=retreve_all_threads()

add_thread(st.session_state["thread_id"])

# side bar ***********************************************
st.sidebar.title("chatbot")
if st.sidebar.button("new chat"):
    reset_chat()

st.sidebar.header("my conversations")
for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"]=thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role="user"
            else:
                role="assistant"
            temp_messages.append({"role":role,"content":message.content})

        st.session_state["message_history"]=temp_messages
#  main ui ************************************************
config={"configurable":{"thread_id":st.session_state["thread_id"]},
        "metadata":{
            "thread_id":st.session_state["thread_id"]
        },
        "run_name":"chat_run"
        }

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("type here...")

if user_input:
    st.session_state["message_history"].append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.text(user_input)

    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in workflow.stream(
                {"messages":[HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages"
                )
        )
    st.session_state["message_history"].append({"role":"assistant","content":ai_message})
