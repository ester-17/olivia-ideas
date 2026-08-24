import streamlit as st

st.set_page_config(
    page_title="OlivIA Ideas",
    page_icon="🧠",
    layout="centered"
)
pages = {
    '': [
        st.Page("./frontend/pages/hero.py", title="OlivIA Ideias", default=True),
    ],
    '💭 Ideias': [
        st.Page("frontend/pages/create.py", title="Criar Ideia"),
    ],
}

navbar = st.navigation(pages, position="top")
navbar.run()