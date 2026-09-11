"""Landing page for OlivIA Ideas."""

import streamlit as st


HERO_CSS = """
<style>
    .hero-title { text-align: center; font-size: 64px; font-weight: bold; margin: 0; }
    .hero-subtitle { color: #4A4A4A; font-size: 38px; font-weight: bold;
        line-height: 50px; margin: 0; padding-bottom: 60px; text-align: center; }
</style>
"""


def render_page() -> None:
    """Render the application landing page."""
    st.markdown(HERO_CSS, unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">OlivIA Ideas</h1>', unsafe_allow_html=True)
    st.markdown(
        '<h2 class="hero-subtitle">Transforme ideias em oportunidades reais</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """Uma plataforma inteligente que transforma uma ideia em um plano claro.

Insira sua ideia e receba uma estrutura 5W2H e uma análise de negócio com apoio
de IA, incluindo público-alvo, riscos, concorrentes e próximos passos."""
    )
    st.divider()
    st.subheader("💭 Comece agora")
    st.write("Crie uma ideia e escolha se deseja somente salvá-la ou analisá-la com IA.")
    if st.button("Criar uma ideia", use_container_width=True):
        st.switch_page("frontend/pages/create.py")


render_page()
