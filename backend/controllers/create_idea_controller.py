from backend.services.idea_service import IdeaService

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
        return self.idea_service.create_idea(payload)

create_idea_controller = CreateIdeaController()