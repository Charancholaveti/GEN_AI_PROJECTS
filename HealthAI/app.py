# import streamlit as st
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_community.llms import Ollama
# import os
# from dotenv import load_dotenv
# load_dotenv()

# os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot with ollama"

# prompt=ChatPromptTemplate(
#     [
#       ("system","You are a helpful assistant,Please respond to user queries"),
#       ("user","Question{question}")
#     ]
# )

# def generate_response(question,engine):
#     llm=Ollama(model=engine)
#     output_parser=StrOutputParser()
#     chain=prompt|llm|output_parser
#     answer=chain.invoke({'question':question})
#     return answer
# st.title("Enhanced Q&A Chatbot With Ollama")


# ## Select the OpenAI model
# # llm=st.sidebar.selectbox("Select Open Source model",["llama3.2:1b"])
# llm="llama3.2:1b"

# # ## Adjust response parameter
# # temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
# # max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# ## MAin interface for user input
# st.write("Goe ahead and ask any question")
# user_input=st.text_input("You:")

# if user_input :
#     response=generate_response(user_input,llm)
#     st.write(response)
# else:
#     st.write("Please provide the user input")


import streamlit as st
import pandas as pd
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "HealthAI with Ollama"

# Define prompt
prompt = ChatPromptTemplate([
    ("system", "You are a helpful medical assistant. Answer clearly and accurately."),
    ("user", "Question: {question}")
])

# Load datasets
try:
    symptom_disease_df = pd.read_csv("symptom_disease.csv")
except:
    symptom_disease_df = None

try:
    with open("disease_medication.json") as f:
        disease_medication = json.load(f)
except:
    disease_medication = {}

# LLM response generator
def generate_response(question, engine="llama3.2:1b"):
    llm = Ollama(model=engine)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer

# Streamlit app setup
st.set_page_config(page_title="HealthAI", page_icon="🩺")
st.title("🩺 HealthAI - Powered by Ollama")
st.markdown("""
Welcome to **HealthAI** – an AI-powered assistant for health questions.
*Note: This is not medical advice. Consult a professional for critical issues.*
""")

# Sidebar for features
feature = st.sidebar.radio("Choose a feature", [
    "Patient Chat 🤖",
    "Symptoms ➝ Disease 🧬",
    "Disease ➝ Medication 💊",
    "Natural Tips 🌿"
])

# Patient Chat
def patient_chat():
    query = st.text_input("Ask your health-related question")
    if query:
        response = generate_response(query)
        st.write(response)

# Symptoms to Disease
def symptoms_to_disease():
    if symptom_disease_df is not None:
        symptoms_input = st.text_input("Enter symptoms (comma-separated)")
        if symptoms_input:
            matched = False
            for _, row in symptom_disease_df.iterrows():
                if all(symptom.strip() in symptoms_input.lower() for symptom in row['symptoms'].lower().split(',')):
                    st.success(f"Possible disease: {row['disease']}")
                    matched = True
                    break
            if not matched:
                st.warning("No exact match found. Try using Patient Chat instead.")
    else:
        st.error("symptom_disease.csv file not found. Please upload it.")

# Disease to Medication
def disease_to_medication():
    disease = st.text_input("Enter a disease")
    if disease:
        meds = None
        for d_name in disease_medication:
            if d_name.lower() == disease.lower():
                meds = disease_medication[d_name]
                break
        if meds:
            st.write("Suggested medications:", ', '.join(meds))
        else:
            st.warning("No medication found for that disease.")

# Natural Tips
def natural_tips():
    disease = st.text_input("Enter a disease")
    if disease:
        query = f"Give natural remedies and lifestyle tips for managing {disease}."
        response = generate_response(query)
        st.write(response)

# Feature selector
if feature == "Patient Chat 🤖":
    patient_chat()
elif feature == "Symptoms ➝ Disease 🧬":
    symptoms_to_disease()
elif feature == "Disease ➝ Medication 💊":
    disease_to_medication()
elif feature == "Natural Tips 🌿":
    natural_tips()