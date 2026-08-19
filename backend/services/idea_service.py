from backend.repositories.idea_repository import IdeaRepository
from backend.services.ai_service import AIService
from backend.services.validation_service import ValidationService

class IdeaService:
    """
    Orchestrates the creation and analysis process of an idea.

    Workflow:
        1. Validate the incoming payload.
        2. Persist the main idea and 5W2H data.
        3. Generate AI analysis if requested.
        4. Save the generated AI analysis.
        5. Return the final result to the controller.
    """

    def __init__(self):
        self.validation_service = ValidationService()
        self.ai_service = AIService()
        self.repository = IdeaRepository()

    def create_idea(self, payload: dict) -> dict:
        """
        Creates a new idea and conditionally generates its AI analysis.
        
        Args:
            payload: A dictionary containing the raw idea data, 5W2H methodology,
            and options sent by the controller.

        Returns:
            A dictionary containing the generated 'idea_id' and an optional
            Markdown 'report' string if requested.
        """
        # 1. Validation
        payload = self.validation_service.validate_payload(payload)
        options = payload["options"]
        show_report = options["show_report"]

        # 2. Save idea
        idea_id = self.repository.create_idea(payload["idea"])

        # 3. AI
        report = None

        if self._should_use_ai(options):
            analysis = self.ai_service.generate(payload)
            self.repository.save_analysis(
                idea_id = idea_id, analysis = analysis
            )

            if show_report:
                report = self.ai_service.to_markdown(analysis)

        # 4. Return results
        return {
            "idea_id": idea_id,
            "report": report
        }

    def _should_use_ai(self, options: dict) -> bool:
        """
        Determines if any AI-powered feature was requested by the user.

        Args:
            options: A dictionary containing the 'use_ai' feature flags.

        Returns:
            True if any AI feature flag is active, False otherwise.
        """
        use_ai = options["use_ai"]
        return (use_ai["title"] or any(use_ai["methodology"].values()))