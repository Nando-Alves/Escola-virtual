import streamlit as st
from core.core_exercises import gerar_exercicio

st.set_page_config(page_title="Gerador de Exercícios e Quiz", layout="centered")
st.title("📚 Gerador de Exercícios")
st.markdown("Crie exercícios personalizados usando inteligência artificial!")

with st.sidebar:
    st.header("Opções de Geração")
    tipo_geracao = st.radio(
        "O que você quer gerar?",
        ("Exercício"),
        help="Escolha entre gerar exercícios com soluções ou questões de quiz de múltipla escolha."
    )
    topico = st.text_input("Qual o tópico/assunto?", "Matemática Financeira", help="Ex: 'Física Quântica', 'Literatura Brasileira', 'Programação Python'")
    nivel = st.selectbox(
        "Qual o nível de dificuldade?",
        ("Básico", "Intermediário", "Avançado"),
        help="Defina a complexidade do conteúdo gerado."
    )
    quantidade = st.slider("Quantas questões/itens?", 1, 10, 3, help="Número de exercícios ou questões de quiz a serem gerados.")

    st.markdown("---")
    gerar_btn = st.button("✨ Gerar Conteúdo")
    st.markdown("---")
    st.info("Desenvolvido com Streamlit e Google Gemini API.")


if gerar_btn:
    st.subheader(f"Conteúdo Gerado de {tipo_geracao}")
    st.markdown("---") 

    if tipo_geracao == "Exercício":
        for i in range(quantidade):
            st.markdown(f"#### Exercício {i+1}")
            with st.spinner(f"Gerando exercício {i+1} de {quantidade}..."):
                exercicio_gerado = gerar_exercicio(topico, nivel)
                st.markdown(exercicio_gerado)
            if i < quantidade - 1: 
                st.markdown("---")
    
else:
    st.info("Selecione as opções na barra lateral e clique em 'Gerar Conteúdo' para ver os exercícios ou quizzes aqui.")