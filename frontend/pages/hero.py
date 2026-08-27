import streamlit as st

# ==========================================
# PAGE CONFIGURATION AND STYLES
# ==========================================

# Custom styles for the hero title and subtitle
HERO_CSS = """
<style>
    .hero-title {
        text-align: center;
        font-weight: bold;
        font-size: 64px;
        margin: 0;
        padding: 10px;
    }
    .hero-subtitle {
        text-align: center;
        font-weight: bold;
        font-size: 38px;
        line-height: 50px;
        padding-bottom: 60px;
        margin: 0;
        color: #4A4A4A;
    }
</style>
"""

st.markdown(HERO_CSS, unsafe_allow_html=True)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    '<h1 class="hero-title">OlivIA Ideias</h1>',
    unsafe_allow_html=True)
st.markdown(
    '<h2 class="hero-subtitle">Transforme ideias em oportunidades reais</h2>', unsafe_allow_html=True    )

st.markdown(
    """Uma plataforma inteligente que ajuda você a sair do **"tenho uma ideia"** para um plano claro e validado.

Insira sua ideia e receba uma análise estruturada com apoio de IA, incluindo:
- **Definição de público-alvo**
- **Organização com metodologia 5W2H**
- **Sugestões de próximos passos práticos**

Você pode gerenciar todo o ciclo das suas ideias: criar, editar, listar e excluir facilmente.""")

st.divider()

# ==========================================
# NAVIGATION AND ACTIONS
# ==========================================

st.subheader("📂 Gerenciar ideias")
st.write(
    "Acesse suas ideias salvas para visualizar, editar ou excluir quando quiser.")

if st.button("📋 Ver minhas ideias", use_container_width=True):
    st.switch_page("pages/listar.py")

st.divider()

st.subheader("💬 Explorar com chat")
st.write(
    "Prefere desenvolver sua ideia de forma interativa?"
    "Converse com a IA, tire dúvidas e evolua seu projeto em tempo real.")

if st.button("👉 Abrir chat de exploração", use_container_width=True):
    st.switch_page("pages/chat.py")

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.header("⚙️ Sobre")
    st.caption("IdeaForge AI / OlivIA Ideas")
    st.caption("Versão Beta 1.0")