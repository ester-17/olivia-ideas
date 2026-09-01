import logging
from backend.services.idea_service import IdeaService

logger = logging.getLogger("olivia.controllers.create_idea")


class CreateIdeaController:
    """Controller responsible for handling idea creation requests.

    It receives data from the presentation layer and delegates the
    business logic to the IdeaService.
    """

    def __init__(self):
        self.idea_service = IdeaService()

    def create_idea(self, payload: dict) -> dict:
        """Creates a new idea.

        Args:
            payload: Dictionary containing the idea data.

        Returns:
            A dictionary containing the created idea information.
        """
        logger.info("Create idea request received")

        result = self.idea_service.create_idea(payload)

        logger.info("Create idea request completed successfully")

        return result

create_idea_controller = CreateIdeaController()