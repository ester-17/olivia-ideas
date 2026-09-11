"""Application entry point for the OlivIA Ideas Streamlit interface."""

import streamlit as st

from backend.utils.logger import setup_logger


setup_logger()

st.set_page_config(
    page_title="OlivIA Ideas",
    page_icon="🧠",
    layout="centered",
)

PAGES = {
    "": [
        st.Page("frontend/pages/hero.py", title="OlivIA Ideas", default=True),
    ],
    "💭 Ideias": [
        st.Page("frontend/pages/create.py", title="Criar ideia"),
    ],
}

st.navigation(PAGES, position="top").run()
