import streamlit as st

from backend.controllers.create_idea_controller import create_idea_controller


# ==================================================
# Constants
# ==================================================

FIELDS = [
    ("what", "What (O que?)", "Ex.: Plataforma para conectar estudantes a empresas para estágios"),
    ("why", "Why (Por quê?)", "Ex.: Resolver um problema recorrente ou atender uma necessidade ainda pouco explorada."),
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

    st.set_page_config(
        page_title="OlivIA Ideias",
        page_icon="🧠",
        layout="centered"
    )

    st.markdown(
        "<h1 style='text-align:center;'>Criar Ideia</h1>",
        unsafe_allow_html=True
    )


# ==================================================
# Form
# ==================================================

def render_form():

    st.subheader("Ideia")

    idea_title = st.text_area(
        "Dê um título à sua ideia",
        placeholder="Ex: OlivIA Ideas",
        height=60
    )

    checkbox_label = (
        "Refinar com IA"
        if idea_title.strip()
        else "Gerar título com IA."
    )

    if idea_title:
        ai_title = st.checkbox(
            "Refinar com IA",
            help=(
                "Se o título estiver vazio, a IA irá gerar um novo. "
                "Caso contrário, ela irá sugerir uma versão aprimorada."
                ))
    
    else:
        ai_title = st.checkbox(
            "Gerar título com IA",
            help=(
                "Se o título estiver vazio, a IA irá gerar um novo. "
                "Caso contrário, ela irá sugerir uma versão aprimorada."
            ))


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

    use_ai = analysis_mode != "Salvar apenas"

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
                if use_ai:
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

        "use_ai": use_ai,

        "show_report": show_report,

        "methodology_data": methodology_data,

        "use_ai": {
            "title": ai_title,
            "methodology": ai_suggestions
        },
    }


# ==================================================
# Payload
# ==================================================

def build_payload(form_data):

    return {

        "idea": {

            "title": form_data["title"].strip(),

            "description": form_data["description"].strip(),

            "methodology": {

                "type": "5w2h",

                "data": form_data["methodology_data"]

            }

        },

        "options": {

            "manual_5w2h": form_data["manual_5w2h"],

            "show_report": form_data["show_report"],

            "use_ai": form_data["use_ai"]

        }

    }

# ==================================================
# Submit
# ==================================================

def submit(payload):

    try:

        response = (
            create_idea_controller.create_idea(payload)
        )

        st.success("Ideia criada com sucesso!")

        if response.get("report"):

            st.markdown(response["report"])

    except Exception as exc:

        st.error(f"Erro: {exc}")


# ==================================================
# Main
# ==================================================

def main():

    configure_page()

    form_data = render_form()

    st.divider()

    if st.button(
        "🚀 Criar ideia",
        use_container_width=True
    ):

        if not form_data["title"].strip():

            st.error(
                "Informe um título para a ideia."
            )

            return

        if not form_data["description"].strip():

            st.error(
                "Informe uma descrição para a ideia."
            )

            return

        payload = build_payload(form_data)

        submit(payload)


if __name__ == "__main__":

    main()