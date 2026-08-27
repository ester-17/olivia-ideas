import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def get_api_key():
    key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError("API key não encontrada.")

    return key


def generate_text(prompt: str) -> str:
    genai.configure(api_key=get_api_key())

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text if response and response.text else "Sem resposta."


def analyze_idea(idea: str) -> str:
    prompt = f"""
    Você é um especialista em startups e produto.

    Analise a ideia abaixo:

    {idea}

    Responda em português, usando markdown estruturado:

    ## Problema
    ## Público-alvo
    ## 5W2H
    ## Concorrentes
    ## Próximos passos
    """

    try:
        return generate_text(prompt)

    except Exception as e:
        return f"❌ Erro ao analisar ideia: {str(e)}"