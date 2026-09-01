import streamlit as st
from backend.utils.logger import setup_logger

setup_logger()

st.set_page_config(
    page_title="OlivIA Ideas",
    page_icon="🧠",
    layout="centered"
)
pages = {
    '': [
        st.Page("./frontend/pages/hero.py", title="OlivIA Ideas", default=True),
    ],
    '💭 Ideias': [
        st.Page("frontend/pages/create.py", title="Criar Ideia"),
    ],
}

navbar = st.navigation(pages, position="top")
navbar.run()