"""Business workflow for creating and optionally analyzing ideas."""

import logging
from typing import Any, Mapping

from backend.repositories.idea_repository import IdeaRepository
from backend.services.ai_service import AIService
from backend.services.validation_service import ValidationService


logger = logging.getLogger("olivia.services.idea")


class IdeaService:
    """Coordinate validation, AI processing, and persistence.

    Attributes:
        validation_service: Service used to validate incoming payloads.
        repository: Repository used to persist created ideas.
        ai_service: Optional AI service, initialized only when it is needed.
    """

    def __init__(
        self,
        validation_service: ValidationService | None = None,
        repository: IdeaRepository | None = None,
        ai_service: AIService | None = None,
    ) -> None:
        """Initialize workflow dependencies.

        Args:
            validation_service: Optional payload validator.
            repository: Optional persistence repository.
            ai_service: Optional preconfigured AI service.
        """
        self.validation_service = validation_service or ValidationService()
        self.repository = repository or IdeaRepository()
        self.ai_service = ai_service

    def create_idea(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Create an idea and process requested AI operations.

        Args:
            payload: Form data containing idea values and processing options.

        Returns:
            A dictionary with ``idea_id`` and an optional Markdown ``report``.
        """
        validated_payload = self.validation_service.validate_payload(payload)
        ai_tasks = self._resolve_ai_tasks(validated_payload)
        analysis: dict[str, Any] | None = None

        if ai_tasks:
            logger.info("AI processing requested | tasks=%s", ai_tasks)
            service = self.ai_service or AIService()
            validated_payload, analysis = service.process(validated_payload, ai_tasks)

        self._assign_methodology_sources(validated_payload, ai_tasks)
        idea_id = self.repository.create(validated_payload["idea"])
        report = None
        if analysis is not None:
            self.repository.save_analysis(idea_id, self._prepare_analysis_for_storage(analysis))
            if validated_payload["options"]["show_report"]:
                report = (self.ai_service or service).to_markdown(analysis)

        logger.info("Idea created | idea_id=%s", idea_id)
        return {"idea_id": idea_id, "report": report}

    def _prepare_analysis_for_storage(self, analysis: Mapping[str, Any]) -> dict[str, Any]:
        """Adapt the AI response to the repository storage schema.

        Args:
            analysis: Validated analysis response from the AI service.

        Returns:
            A dictionary with the numeric score and separate analysis details.
        """
        return {
            "score": analysis["viability"],
            "analysis_data": {
                key: value for key, value in analysis.items() if key != "viability"
            },
        }

    def _assign_methodology_sources(
        self, payload: dict[str, Any], ai_tasks: Mapping[str, Any]
    ) -> None:
        """Assign a persistable source to every 5W2H field.

        A field is ``AI`` if it was generated or refined by an AI methodology
        task. Every unchanged manual field is ``USER``. The obsolete
        ``USER_EDITED_AI`` value is never produced.

        Args:
            payload: Validated payload whose methodology receives the source map.
            ai_tasks: Resolved AI operations for the current request.
        """
        fields = self.validation_service.REQUIRED_5W2H_FIELDS
        methodology_task = ai_tasks.get("methodology")
        ai_fields = set(fields) if methodology_task == "generate" else set()
        if isinstance(methodology_task, Mapping):
            ai_fields.update(methodology_task)

        payload["idea"]["methodology"]["sources"] = {
            field: "AI" if field in ai_fields else "USER" for field in fields
        }

    def _resolve_ai_tasks(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Resolve requested AI operations from a validated payload.

        Args:
            payload: Validated creation payload.

        Returns:
            A mapping of AI operations and their generation/refinement actions.
        """
        idea = payload["idea"]
        options = payload["options"]
        ai_options = options["ai_options"]
        tasks: dict[str, Any] = {}

        if ai_options["title"]:
            tasks["title"] = "refine" if idea["title"] else "generate"

        if not options["manual_5w2h"]:
            tasks["methodology"] = "generate"
        else:
            methodology_data = idea["methodology"]["data"]
            methodology_tasks = {
                field: "refine" if methodology_data[field] else "generate"
                for field, requested in ai_options["methodology"].items()
                if requested
            }
            if methodology_tasks:
                tasks["methodology"] = methodology_tasks

        if options["generate_analysis"]:
            tasks["analysis"] = True
        return tasks
