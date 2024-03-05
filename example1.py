import os
import streamlit as st
import os
import streamlit as st
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# ... (to_markdown function definition) ...

# Manage environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")

# Streamlit UI
st.title("Celebrity Search Results")
user_query = st.text_input("Give celebrity name") 

# Prompt Template 
new_prompt_template = PromptTemplate(
    input_variables=["name"], 
    template="Tell me about the celebrity {name}"
)

# LLMs
if user_query:
    try:
        # LLM Cache setup
        llm_cache = InMemoryCache()  
        set_llm_cache(llm_cache)

        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        chain = LLMChain(llm=llm, prompt=new_prompt_template, verbose=True) 
        response = chain.run(user_query) 
        st.write((response)) 

    except Exception as e: 
        st.write("An error occurred:", e) 

