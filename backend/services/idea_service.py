from backend.repositories.idea_repository import IdeaRepository
from backend.services.ai_service import AIService
from backend.services.validation_service import ValidationService

import logging

logger = logging.getLogger("olivia.services.idea")

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
        logger.debug("Initializing IdeaService")

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

        logger.info("Starting idea creation")

        # 1. Validation
        logger.debug("Validating idea payload")

        payload = self.validation_service.validate_payload(payload)
        options = payload["options"]
        show_report = options["show_report"]

        logger.debug("Payload validated successfully")

        # 2. Save idea
    
        logger.debug("Persisting idea")

        idea_id = self.repository.create(payload["idea"])

        logger.info("Idea persisted successfully | idea_id: %s", idea_id)

        # 3. AI
        report = None


        if self._should_use_ai(options):
            # 🚧 TEMPORARIO - Later change to debug
            logger.info("AI features requested")

            analysis = self.ai_service.generate(payload)

            logger.info("AI analysis generated successfully | idea_id: %s", idea_id)

            logger.debug("Persisting AI analysis | idea_id: %s", idea_id)

            self.repository.save_analysis(
                idea_id = idea_id, analysis = analysis
            )
            logger.info("AI analysis persisted successfully | idea_id: %s", idea_id)

            if show_report:
                logger.debug("Generating Markdown report | idea_id: %s", idea_id)
                report = self.ai_service.to_markdown(analysis)

        logger.info("Idea creation completed successfully | idea_id: %s", idea_id)
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
        logger.debug("Checking if AI features should be used")
        
        use_ai = options["use_ai"]
        return (use_ai["title"] or any(use_ai["methodology"].values()))