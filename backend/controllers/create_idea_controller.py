"""Controller for idea creation requests."""

import logging
from typing import Any, Mapping

from backend.services.idea_service import IdeaService


logger = logging.getLogger("olivia.controllers.create_idea")


class CreateIdeaController:
    """Delegate idea creation requests from the presentation layer.

    Attributes:
        idea_service: Service that executes the idea-creation workflow.
    """

    def __init__(self, idea_service: IdeaService | None = None) -> None:
        """Initialize the controller.

        Args:
            idea_service: Optional service instance for dependency injection.
        """
        self.idea_service = idea_service or IdeaService()

    def create_idea(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Create an idea from a presentation-layer payload.

        Args:
            payload: Untrusted request data from the Streamlit form.

        Returns:
            The identifier of the created idea and an optional Markdown report.
        """
        logger.info("Create idea request received")
        result = self.idea_service.create_idea(payload)
        logger.info("Create idea request completed | idea_id=%s", result["idea_id"])
        return result


create_idea_controller = CreateIdeaController()
