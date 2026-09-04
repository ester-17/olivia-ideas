OUTPUT_FORMAT_PROMPT = """
## FORMATO DE RESPOSTA

Retorne SOMENTE um JSON válido.

Utilize a seguinte estrutura quando os respectivos campos
forem solicitados:

{
    "title": "...",

    "methodology": {
        "what": "...",
        "why": "...",
        "where": "...",
        "when": "...",
        "who": "...",
        "how": "...",
        "how_much": "..."
    },

    "analysis": {
        "problem": "...",
        "viability": 0,
        "target_audience": "...",
        "risks": [],
        "competitors": [],
        "next_steps": []
    }
}

Inclua somente os blocos solicitados pelas tarefas.
Não altere campos que não foram solicitados.
"""