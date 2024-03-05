import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI 
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from constants import GOOGLE_API_KEY
import pathlib
import textwrap3
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from langchain.chains import LLMChain,SequentialChain
import re
from langchain.memory import ConversationBufferMemory # To remember the conversation

def to_markdown(response):
    text = response.content  # Extract the text content 

    # Regular expression to remove unwanted characters
    text = re.sub(r"[^\w\s\n]", "", text)  

    # Replace newlines with markdown-style line breaks
    text = text.replace('\n', '\n\n') 

    return text 


# Manage environment variables 
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")

 
# Streamlit UI
st.title("Life Lines of Celebrities")
st.subheader("Celebrity Insights on Philosophy, Childhood Aspirations, and Money Matters")
user_query = st.text_input("Give Celebrity name:")

first_input_template = PromptTemplate(
    input_variables=["name"],
    template="Tell me about the celebrity {name}"
)

llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest", google_api_key=GOOGLE_API_KEY)

 

person_memory = ConversationBufferMemory(input_key='name',memory_key='career_history')
philosophy_memory = ConversationBufferMemory(input_key='name',memory_key='philosophy_history')
money_memory = ConversationBufferMemory(input_key='name',memory_key='Money_history')

chain1 = LLMChain(llm=llm,prompt=first_input_template,verbose=True,output_key='person',memory=person_memory)

second_input_template = PromptTemplate(
    input_variables=["name"],
    template="Tell me the philosophy of life, childhood goal {name}  "
)
chain2 = LLMChain(llm=llm,prompt=second_input_template,verbose=True,output_key='philosophy',memory=philosophy_memory)

third_input_template = PromptTemplate(
    input_variables=["name"],
    template="Tell me about, how they look at money and , also perspective about money of {name}  "
)

chain3 = LLMChain(llm=llm,prompt=third_input_template,verbose=True,output_key='About Money',memory=money_memory)

parent_chain = SequentialChain(chains=[chain1,chain2,chain3],input_variables=['name'],output_variables=['person','philosophy','About Money'],verbose=True)
if user_query:
    try:
 #       response = parent_chain.run(user_query)  #sued when simplesequentialchain, chain
        response = parent_chain({"name":user_query})
        st.write(response)

        with st.expander("Philosophy"):
            st.info(philosophy_memory.buffer)
        
        with st.expander("About Money"):
            st.info(money_memory.buffer)
    except Exception as e:  
        st.write("An error occurred:", e) 

 