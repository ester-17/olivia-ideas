OUTPUT_FORMAT_PROMPT = """
## FORMATO DE RESPOSTA

Retorne SOMENTE um JSON válido.

Utilize somente os blocos correspondentes às tarefas solicitadas.

### Título
Se a tarefa de título for solicitada:

{
    "title": "..."
}

### 5W2H

Se a tarefa de título for solicitada:
{
    "fivew2h": {
        "what": "...",
        "why": "...",
        "where": "...",
        "when": "...",
        "who": "...",
        "how": "...",
        "how_much": "..."
    }
}

### Análise

Se a análise for solicitada:
{
    "analysis": {
        "problem": "...",
        "viability": 0,
        "target_audience": "...",
        "risks": [],
        "competitors": [],
        "next_steps": []
    }
}

Não inclue blocos que não foram solicitados.
Não altere informações que não fazem parte da tarefa.
Não adicione explicações, Markdown ou texto fora do JSON.
"""