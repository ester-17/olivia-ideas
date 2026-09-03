import logging
import streamlit as st

from backend.controllers.create_idea_controller import create_idea_controller

logger = logging.getLogger("olivia.frontend.create")

# ==================================================
# Constants
# ==================================================

FIELDS = [
    ("what",
     "What (O que?)",
     "Ex.: Plataforma para conectar estudantes a empresas para estágios"
     ),
    ("why",
     "Why (Por quê?)",
     "Ex.: Resolver um problema recorrente ou atender uma necessidade ainda pouco explorada."),
    ("where", "Where (Onde?)", "Ex.: Aplicativo, site, empresa, escola ou qualquer ambiente onde a solução será utilizada."),
    ("when", "When (Quando?)", "Ex.: Lançamento em 6 meses, implantação gradual ou execução imediata."),
    ("who", "Who (Quem?)", "Ex.: Estudantes, pequenas empresas, profissionais autônomos ou consumidores em geral."),
    ("how", "How (Como?)", "Ex.: Desenvolvimento de software, automação de processos, uso de IA ou prestação de serviços."),
    ("how_much", "How Much (Quanto?)", "Ex.: R$ 5.000, sem custos iniciais ou aproximadamente 100 horas de desenvolvimento."),
]

# ==================================================
# Page
# ==================================================

def configure_page():
    """Render the create-idea page title."""

    st.markdown(
        "<h1 style='text-align:center;'>Criar Ideia</h1>",
        unsafe_allow_html=True
    )

# ==================================================
# Form
# ==================================================

def render_form():
    """Render the idea creation form and return its data as a dictionary."""

    st.subheader("Ideia")

    idea_title = st.text_area(
        "Dê um título à sua ideia",
        placeholder="Ex: OlivIA Ideas",
        height=60,
    )

    checkbox_label = (
        "Refinar com IA"
        if idea_title.strip()
        else "Gerar título com IA."
    )

    ai_title = st.checkbox(
        checkbox_label,
        help=(
            "Se o título estiver vazio, a IA irá gerar um novo. "
            "Caso contrário, ela irá sugerir uma versão aprimorada."
            ),
            value=not idea_title.strip()
        )


    idea_description = st.text_area(
        "Descreva sua ideia",
        placeholder="Ex: Um sistema que transforma ideias em oportunidades...",
        height=150
    )

    st.divider()

    st.subheader("Análise")

    analysis_mode = st.radio(
        "Como deseja processar esta ideia?",
        (
            "Salvar apenas",
            "Salvar e analisar com IA",
            "Salvar, analisar e exibir relatório"
        )
    )

    generate_analysis = analysis_mode != "Salvar apenas"
    show_report = analysis_mode == "Salvar, analisar e exibir relatório"

    manual_5w2h = st.radio(
        "Como deseja preencher o 5W2H?",
        (
            "Automático",
            "Manual"
        )
    )

    methodology_data = {
        field: ""
        for field, _, _ in FIELDS
    }

    ai_suggestions = {
        field: False
        for field, _, _ in FIELDS
    }

    if manual_5w2h == "Manual":

        st.divider()

        st.subheader("5W2H")

        st.info(
            "Campos vazios serão preenchidos automaticamente pela IA.\n\n"
            "Caso deseje melhorar um campo já preenchido, marque "
            "'Refinar com IA'."
        )

        for field, label, placeholder in FIELDS:

            text = st.text_area(
                label,
                placeholder=placeholder,
                height=70,
                key=f"{field}_text"
            ).strip()

            methodology_data[field] = text
            if text:
                if manual_5w2h == "Manual":
                    ai_suggestions[field] = (st.checkbox(
                            "Refinar com IA",
                            key=f"{field}_ai"
                        )
                    )
                        
                else:
                    ai_suggestions[field] = False            

    return {

        "title": idea_title,
        "description": idea_description,
        "manual_5w2h": manual_5w2h == "Manual",
        "generate_analysis": generate_analysis,
        "show_report": show_report,
        "methodology_data": methodology_data,
        "ai_options": {
            "title": ai_title,
            "methodology": ai_suggestions
        },
    }


# ==================================================
# Payload
# ==================================================

def build_payload(form_data):
    """Build the payload expected by the create-idea controller."""

    payload = {

        "idea": {

            "title": form_data["title"].strip(),
            "description": form_data["description"].strip(),
            "methodology": {
                "type": "5w2h",
                "data": form_data["methodology_data"]
            },
        },
        "options": {
            "manual_5w2h": form_data["manual_5w2h"],
            "generate_analysis": form_data["generate_analysis"],
            "show_report": form_data["show_report"],
            "ai_options": form_data["ai_options"]
        },
    }

    logger.debug(
        "Idea payload built | manual_5w2h=%s | generate_analysis=%s | " "show_report=%s | ai_title=%s",
        payload["options"]["manual_5w2h"],
        payload["options"]["generate_analysis"],
        payload["options"]["show_report"],
        payload["options"]["ai_options"]["title"], 
        )

    return payload

# ==================================================
# Submit
# ==================================================

def submit(payload):
    """Submit an idea payload to the create-idea controller."""

    try:
        options = payload["options"]

        logger.info(
            "Submitting payload to controller | generate_analysis:%s | show_report:%s",
            payload["options"]["generate_analysis"],
            payload["options"]["show_report"],
            options["ai_options"]["title"],
        )

        response = (create_idea_controller.create_idea(payload))

        logger.info(
            "Idea submitted successfully | idea_id: %s ", response("idea_id"))
        st.success("Ideia criada com sucesso!")

        if response.get("report"):
            logger.debug("Displaying AI report")
            st.markdown(response["report"])

    except Exception:

        logger.exception("Failed to submit idea")
        st.error(f"Não foi possível criar a ideia.")


# ==================================================
# Main
# ==================================================

def main():
    """Render and handle idea creation."""

    configure_page()
    form_data = render_form()

    st.divider()

    if st.button(
        "Criar ideia",
        use_container_width=True
    ):
        logger.info("Create idea button clicked.")

        if not form_data["description"].strip():

            st.error(
                "Informe uma descrição para a ideia."
            )
            logger.warning("Form submission rejected: description field is empty.") 

            return

        payload = build_payload(form_data)
        # TALVEZ ADICIONAR UM PRINT DO PAYLOAD COMPLETO PARA DEBUGAR MELHOR

        submit(payload)


if __name__ == "__main__":
    main()