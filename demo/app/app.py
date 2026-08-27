import streamlit as st
from gemini_service import analyze_idea


st.set_page_config(
    page_title="IdeaForge AI",
    page_icon="💡",
    layout="centered"
)

st.title("💡 IdeaForge AI")
st.caption("Transforme ideias em oportunidades reais")




idea = st.text_area(
    "Descreva sua ideia",
    placeholder="Ex: Um app de controle de ponto com geolocalização...",
    height=150
)

st.info("💡 Dica:\nSeja específico na sua ideia.")


if st.button("🚀 Analisar ideia", use_container_width=True):
    if idea.strip():
        with st.spinner("Analisando sua ideia..."):
            result = analyze_idea(idea)
        
        st.subheader("📊 Resultado")
        st.markdown(result)
    else:
        st.warning("Digite uma ideia primeiro.")

with st.sidebar:
    st.header("⚙ Sobre")
    st.write("IdeaFoge AI")
    st.write("Versão 1.0")
