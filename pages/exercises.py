import streamlit as st
import google.generativeai as genai
import os

# --- Configuração da API Gemini ---
# Tenta carregar a chave de API APENAS de uma variável de ambiente
api_key = os.environ.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Chave de API do Google não encontrada. Por favor, configure a variável de ambiente `GOOGLE_API_KEY`.")
    st.stop() # Para o aplicativo se a chave não for encontrada

st.set_page_config(page_title="Gerador de Exercícios e Quiz", layout="centered")
st.title("📚 Gerador de Exercícios e Quiz com Gemini")
st.markdown("Crie exercícios e questões de quiz personalizados usando inteligência artificial!")

# --- Funções de Geração com Gemini (Mesmas que antes) ---

def gerar_exercicio(topico, nivel):
    # ... (código da função gerar_exercicio)
    prompt = f"""
    Crie um exercício de {topico} de nível {nivel}. Inclua o problema e a solução detalhada.
    O problema deve ser desafiador, mas claro.
    A solução deve ser passo a passo e fácil de entender.

    Formato esperado:
    **Problema:**
    [Seu problema aqui]

    **Solução:**
    [Sua solução detalhada aqui]
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def gerar_quiz(topico, nivel):
    # ... (código da função gerar_quiz)
    prompt = f"""
    Crie uma pergunta de quiz de múltipla escolha sobre {topico} de nível {nivel}.
    A pergunta deve ser clara e as opções devem ser plausíveis, mas apenas uma correta.
    Inclua a pergunta, 4 opções (A, B, C, D) e a resposta correta.

    Formato esperado:
    **Pergunta:**
    [Sua pergunta aqui]

    **Opções:**
    A) [Opção A]
    B) [Opção B]
    C) [Opção C]
    D) [Opção D]

    **Resposta Correta:**
    [Letra da resposta correta, ex: B)]
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# --- Interface do Streamlit (Mesma que antes) ---

# Sidebar para opções de geração
with st.sidebar:
    st.header("Opções de Geração")
    tipo_geracao = st.radio(
        "O que você quer gerar?",
        ("Exercício", "Quiz"),
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


# Área de exibição do conteúdo
if gerar_btn:
    st.subheader(f"Conteúdo Gerado de {tipo_geracao}")
    st.markdown("---") # Linha divisória para separar o cabeçalho do conteúdo

    if tipo_geracao == "Exercício":
        for i in range(quantidade):
            st.markdown(f"#### Exercício {i+1}")
            with st.spinner(f"Gerando exercício {i+1} de {quantidade}..."):
                exercicio_gerado = gerar_exercicio(topico, nivel)
                st.markdown(exercicio_gerado)
            if i < quantidade - 1: 
                st.markdown("---")
    elif tipo_geracao == "Quiz":
        for i in range(quantidade):
            st.markdown(f"#### Questão {i+1}")
            with st.spinner(f"Gerando questão {i+1} de {quantidade}..."):
                quiz_gerado = gerar_quiz(topico, nivel)
                st.markdown(quiz_gerado)
            if i < quantidade - 1: # Adiciona uma linha divisória entre as questões
                st.markdown("---")
else:
    st.info("Selecione as opções na barra lateral e clique em 'Gerar Conteúdo' para ver os exercícios ou quizzes aqui.")