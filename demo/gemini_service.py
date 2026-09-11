"""Gemini integration used by the standalone demonstration app."""

import logging
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

logger = logging.getLogger(__name__)

load_dotenv()

PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-2.5-flash"


def get_api_key() -> str:
    """Return the Gemini API key from Streamlit secrets or the environment.

    Returns:
        Configured Gemini API key.

    Raises:
        ValueError: If no API key is configured.
    """
    key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not key:
        logger.error("GEMINI_API_KEY não foi encontrada nos segredos ou .env")
        raise ValueError("Chave de API do Gemini não configurada.")

    return key


def generate_text(prompt: str) -> str:
    """Generate text, using the fallback model for transient API errors.

    Args:
        prompt: Instruction sent to Gemini.

    Returns:
        Text produced by the model.

    Raises:
        RuntimeError: If every configured model fails.
    """
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]

    for model in models_to_try:
        try:
            logger.info("Sending request to Gemini model | model=%s", model)
            
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if response and response.text:
                return response.text

            raise ValueError("Resposta vazia retornada pela IA.")

        except errors.APIError as err:
            # Captura erros nativos da API da Google (ex: HTTP 503, 429)
            logger.warning(
                "Gemini API error | model=%s | code=%s | message=%s",
                model,
                err.code,
                err.message,
            )

            # Se for indisponibilidade (503 / 429) e ainda houver modelos de fallback, tenta o próximo
            if err.code in (503, 429) and model != models_to_try[-1]:
                logger.info("Trying fallback model after transient API error")
                continue
            
            # Se não houver mais modelos de fallback ou for outro tipo de erro da API
            raise RuntimeError("O serviço de Inteligência Artificial está temporariamente sobrecarregado. Tente novamente em alguns instantes.") from None

        except Exception as exc:
            # Captura outros erros genéricos (ex: erro de conexão) sem vazar traces
            logger.exception("Unexpected Gemini communication error | model=%s", model)
            raise RuntimeError("Não foi possível processar sua solicitação no momento.") from None

    raise RuntimeError("Nenhum modelo de IA respondeu à solicitação.")


def analyze_idea(idea: str) -> str:
    """Analyze an idea and return a safe, Markdown-formatted result.

    Args:
        idea: User-provided idea description.

    Returns:
        Analysis result or an appropriate user-facing error message.
    """
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
        # Exibe apenas a mensagem tratada e segura na vitrine do MVP
        return f"⚠️ **Aviso:** {str(e)}"
    except Exception:
        # Caso ocorra algo totalmente fora do previsto
        return "❌ Ocorreu uma falha ao gerar a análise da ideia. Por favor, tente novamente mais tarde."
