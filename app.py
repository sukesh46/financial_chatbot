import streamlit as st
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

print('1')

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit_scrollable_textbox as stx


from doc_processing import process_pdf,vectordb,justnames
from tool_list import repl
from agent import agent_init

@st.cache_resource
def give_agent(files):
    paths,names=process_pdf(files)
    y = vectordb(paths,names)
    tools = repl(y)
    agent=agent_init(tools)
    return agent


os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]


    # app config
st.set_page_config(page_title="Fin bot", page_icon="🤖")
st.title("Fin bot")

files = st.file_uploader(label="Upload your pdfs here", accept_multiple_files=True,type="pdf")

if(files != None):

    agent = give_agent(files=files)

    stx.scrollableTextbox("Hello, I am  Finbot. How can I help you?")
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query!="":
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            response = agent.run(user_query)
            stx.scrollableTextbox(response)



    

