import logging

from backend.services.prompts import (
    BASE_PROMPT,
    TITLE_PROMPTS,
    build_methodology_prompt,
    ANALYSIS_PROMPT,
    OUTPUT_FORMAT_PROMPT,
)

logger = logging.getLogger("olivia.services.prompt")

class PromptService:
    """Builds dynamic modular prompts for single-pass AI requests."""
    def build(self, payload: dict, ai_tasks: dict) -> str:
        """Build a single prompt from the requested AI tasks.
        
        Args:
            payload: Validated idea payload.
            ai_tasks: AI operations resolved by IdeaService.
            
        Returns:
            Complete prompt ready to be sent to the AI model.
        """
        logger.debug("Building AI prompt | tasks=%s", ai_tasks)
        blocks = [
            BASE_PROMPT,
            self._build_idea_context(payload),
        ]

        # Title
        if "title" in ai_tasks:
            action = ai_tasks["title"]
            logger.debug(
                "Adding title prompt block | action=%s", action
            )

            blocks.append(TITLE_PROMPTS[action])

        # Methodology
        if "methodology" in ai_tasks:
            logger.debug("Adding methodology prompt block")
            blocks.append(
                build_methodology_prompt(ai_tasks["methodology"])
            )

        # Analysis
        if ai_tasks.get("analysis"):
            logger.debug("Adding analysis prompt block")

            blocks.append(ANALYSIS_PROMPT)

        blocks.append(OUTPUT_FORMAT_PROMPT)

        prompt = "\n\n".join(blocks)

        logger.debug(
            "AI prompt build successfully | blocks=%s | length=%s",
            len(blocks),len(prompt)
        )

        return prompt

    def _build_idea_context(self, payload: dict) -> str:
        """Build the idea context included in the AI prompt."""

        idea =payload["idea"]
        methodology = idea.get("methodology",{}).get("data", {})

        return f"""
## DADOS DA IDEIA

Título:
{idea.get("title", "")}

Descrição:
{idea.get("description", "")}

## 5W2H ATUAL

What:
{methodology.get("what", "")}

Why:
{methodology.get("why", "")}

Where:
{methodology.get("where", "")}

When:
{methodology.get("when", "")}

Who:
{methodology.get("who", "")}

How:
{methodology.get("how", "")}

How Much:
{methodology.get("how_much", "")}
"""