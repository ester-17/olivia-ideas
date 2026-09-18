"""Prompt fragments for generating or refining a 5W2H methodology."""

from collections.abc import Mapping


METHODOLOGY_FIELDS = {
    "what": "O que?",
    "why": "Por quê?",
    "where": "Onde?",
    "when": "Quando?",
    "who": "Quem?",
    "how": "Como?",
    "how_much": "Quanto?"
}


def build_methodology_prompt(tasks: str | Mapping[str, str]) -> str:
    """Build instructions for requested 5W2H operations.

    Args:
        tasks: ``"generate"`` for all fields or a mapping from field to action.

    Returns:
        Prompt fragment describing only the requested methodology work.

    Raises:
        ValueError: If a field action is not ``generate`` or ``refine``.
    """
    if tasks == "generate":
        return """
## 5W2H

O 5W2H não foi preenchido manualmente.

Crie todos os campos do 5W2H com base no
título e na descrição da ideia.

Preencha:

- what
- why
- where
- when
- who
- how
- how_much
"""

    instructions = []

    for field, action in tasks.items():

        field_name = METHODOLOGY_FIELDS.get(
            field,
            field
        )

        if action == "generate":
            instructions.append(
                f"- {field} ({field_name}): "
                "gere uma resposta com base no contexto da ideia."
            )

        elif action == "refine":
            instructions.append(
                f"- {field} ({field_name}): "
                "refine o conteúdo existente mantendo sua intenção."
            )
        else:
            raise ValueError(f"Unsupported methodology action: {action}")

    return f"""
## 5W2H

Processar somente os campos explicitamente solicitados.

Não altere os demais campos.

{chr(10).join(instructions)}
"""
