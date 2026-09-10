import os
import logging
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

logger = logging.getLogger(__name__)

load_dotenv()

PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-2.5-flash"

def get_api_key() -> str:
    key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        logger.error("GEMINI_API_KEY não foi encontrada nos segredos ou .env")
        raise ValueError("Chave de API do Gemini não configurada.")
    return key

def generate_text(prompt: str) -> str:
    """Gera texto utilizando o modelo principal e aciona fallback em caso de alta demanda (503)."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]

    for model in models_to_try:
        try:
            logger.info(f"Enviando requisição para o modelo Gemini: {model}")
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if response and response.text:
                return response.text
            
            raise ValueError("Resposta vazia retornada pela IA.")

        except errors.APIError as err:
            
            # Captura erros nativos da API da Google (ex: HTTP 503, 429)
            logger.warning(f"Erro na API do Gemini com o modelo {model}: {err.code} - {err.message}")

            # Em caso de indisponibilidade (503/429) e ainda houver modelos de fallback, tenta o próximo
            if err.code in (503, 429) and model != models_to_try[-1]:
                logger.info(f"Tentando modelo de contingência devido a sobrecarga no {model}...")
                continue

            # Caso não haja mais modelos de fallback ou for outro tipo de erro da API
            raise RuntimeError("O serviço de Inteligência Artificial está temporariamente sobrecarregado. Tente novamente em alguns instantes.") from None
        
        except Exception as exc:
            logger.exception(f"Falha inesperada ao comunicar com o Gemini utilizando {model}")
            raise RuntimeError("Não foi possível processar sua solicitação no momento.") from None

    return "Sem resposta."

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

    except RuntimeError as e:
        return f"⚠️ **Aviso:** {str(e)}"

    except Exception:
        return "❌ Ocorreu uma falha ao gerar a análise da ideia. Por favor, tente novamente mais tarde."