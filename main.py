## Integrate our code with Google api
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI 
import google.generativeai as genai

from constants import GOOGLE_API_KEY

import pathlib

import textwrap3
 
import google.generativeai as genai

 

from IPython.display import display
from IPython.display import Markdown


import re

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
st.title("Langchain Demo With Google PRO")
user_query = st.text_input("Ask your question:")

if user_query:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest", google_api_key=GOOGLE_API_KEY)
        response = llm.invoke(user_query)  
        st.write(to_markdown(response))  
    except Exception as e:  
        st.write("An error occurred:", e) 
