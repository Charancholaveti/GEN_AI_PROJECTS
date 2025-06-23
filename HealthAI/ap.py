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
st.title("🧠 HealthAI: Intelligent Healthcare Assistant")
st.markdown("""
Welcome to **HealthAI** – An AI-powered assistant for health questions.
*Note: This is not medical advice. Consult a professional for critical issues.*
""")

# Sidebar for features
feature = st.sidebar.selectbox("Choose a feature", [
    "Patient Chat 🤖",
    "Symptoms ➝ Disease 🧬",
    "Disease ➝ Medication 💊",
    "Natural Tips 🌿"
])
st.sidebar.markdown("---")
st.sidebar.caption("Powered by IBM Granite · via Hugging Face")
# Patient Chat
def patient_chat():
    query = st.text_input("Ask your health-related question")
    if query:
        response = generate_response(query)
        st.write(response)
        st.caption("⚠️ This is for informational use only.")

# Symptoms to Disease
def symptoms_to_disease():
    if symptom_disease_df is not None:
        symptoms_input = st.text_input("Enter symptoms (comma-separated)")
        if symptoms_input:
            matched = False
            for _, row in symptom_disease_df.iterrows():
                if all(symptom.strip() in symptoms_input.lower() for symptom in row['symptoms'].lower().split(',')):
                    st.success(f"Possible disease: {row['disease']}")
                    st.caption("⚠️ This is for informational use only.")
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
            st.caption("⚠️ This is for informational use only.")
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
st.markdown("---")
st.caption("© 2025 HealthAI · Streamlit + Hugging Face + IBM Granite")