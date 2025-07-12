import streamlit as st 
from core.core_resume import gerar_resumo

st.set_page_config(page_title="Gerador de Resumos", layout="centered")
st.title("📚 Gerador de Resumos")
st.markdown("Crie resumos sobre qualquer conteúdo com a inteligência artificial!")

with st.sidebar:
    st.header("Escolha o Conteúdo")
    topico = st.text_input("Qual o conteudo do Resumo?")
    st.markdown("---")
    gerar_btn = st.button("✨ Gerar Conteúdo")
    st.markdown("---")

if gerar_btn:
    st.subheader(f"Conteúdo Gerado de {topico}")
    st.markdown("---") 

    with st.spinner(f"Gerando resumo..."):
        resumo_gerado = gerar_resumo(topico)
        st.markdown(resumo_gerado)       
else:
    st.info("Selecione as opções na barra lateral e clique em 'Gerar Conteúdo' para gerar seu resumo.") 
    