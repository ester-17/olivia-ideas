import logging

from backend.repositories.idea_repository import IdeaRepository
from backend.services.ai_service import AIService
from backend.services.validation_service import ValidationService


logger = logging.getLogger("olivia.services.idea")


class IdeaService:
    """
    Orchestrates the creation and analysis process of an idea.

    Workflow:
        1. Validate the incoming payload.
        2. Resolve AI processing requirements.
        3. Execute AI generation/refinement and analysis in a single request.
        4. Persist the main idea and 5W2H data.
        5. Persist the AI analysis, if generated.
        6. Return the final result to the controller.
    """

    def __init__(self):
        """Initialize the services and repository."""

        logger.debug("Initializing IdeaService")

        self.validation_service = ValidationService()
        self.ai_service = AIService()
        self.repository = IdeaRepository()

    def create_idea(self, payload: dict) -> dict:
        """
        Create a new idea and process requested AI features.

        Args:
            payload: Dictionary containing the idea data and processing options.

        Returns:
            Dictionary containing the created idea ID and an optional report.
        """

        logger.info("Starting idea creation")

        # ==================================================
        # 1. Validation
        # ==================================================

        logger.debug("Validating idea payload")

        payload = self.validation_service.validate_payload(payload)

        options = payload["options"]

        logger.debug(
            "Payload structure and types validated successfully"
        )

        # ==================================================
        # 2. Resolve AI tasks
        # ==================================================

        ai_tasks = self._resolve_ai_tasks(payload)

        if ai_tasks:
            logger.info(
                "AI processing requested | tasks=%s",
                ai_tasks
            )

            payload, analysis_data = self.ai_service.process(
                payload,
                ai_tasks
            )

        else:
            logger.debug("No AI processing requested")
            analysis_data = None

        # ==================================================
        # 3. Persist idea
        # ==================================================

        logger.debug("Persisting idea")

        idea_id = self.repository.create(
            payload["idea"]
        )

        logger.info(
            "Idea persisted successfully | idea_id=%s",
            idea_id
        )

        # ==================================================
        # 4. Persist AI analysis
        # ==================================================

        report = None

        if analysis_data:

            logger.debug(
                "Persisting AI analysis | idea_id=%s",
                idea_id
            )

            self.repository.save_analysis(
                idea_id=idea_id,
                analysis=analysis_data
            )

            logger.info(
                "AI analysis persisted successfully | idea_id=%s",
                idea_id
            )

            # ==================================================
            # 5. Generate report
            # ==================================================

            if options.get("show_report", False):

                logger.debug(
                    "Generating Markdown report | idea_id=%s",
                    idea_id
                )

                report = self.ai_service.to_markdown(
                    analysis_data
                )

        logger.info(
            "Idea creation completed successfully | idea_id=%s",
            idea_id
        )

        return {
            "idea_id": idea_id,
            "report": report,
        }

    # ==================================================
    # AI Task Resolution
    # ==================================================

    def _resolve_ai_tasks(self, payload: dict) -> dict:
        """
        Determine which operations should be performed by AI.

        The method distinguishes between generating new content,
        refining existing content, and generating a complete analysis.

        Args:
            payload: Validated idea creation payload.

        Returns:
            Dictionary describing the AI operations to execute.
        """

        idea = payload["idea"]
        options = payload["options"]
        ai_options = options.get("ai_options", {})

        tasks = {}

        # ==================================================
        # Title
        # ==================================================

        if ai_options.get("title", False):

            title = idea["title"].strip()

            action = "refine" if title else "generate"

            tasks["title"] = action

            logger.debug(
                "AI title task resolved | action=%s",
                action
            )

        # ==================================================
        # 5W2H
        # ==================================================

        manual_5w2h = options.get(
            "manual_5w2h",
            False
        )

        if not manual_5w2h:

            tasks["methodology"] = "generate"

            logger.debug(
                "AI methodology task resolved | action=generate"
            )

        else:

            methodology_options = ai_options.get(
                "methodology",
                {}
            )

            methodology_data = (
                idea
                .get("methodology", {})
                .get("data", {})
            )

            methodology_tasks = {}

            for field, requested in methodology_options.items():

                if not requested:
                    continue

                value = methodology_data.get(
                    field,
                    ""
                ).strip()

                action = "refine" if value else "generate"

                methodology_tasks[field] = action

                logger.debug(
                    "AI methodology task resolved | "
                    "field=%s | action=%s",
                    field,
                    action
                )

            if methodology_tasks:

                tasks["methodology"] = methodology_tasks

        # ==================================================
        # Full Analysis
        # ==================================================

        if options.get("generate_analysis", False):

            tasks["analysis"] = True

            logger.debug(
                "AI analysis task resolved | generate_analysis=True"
            )

        return tasks
