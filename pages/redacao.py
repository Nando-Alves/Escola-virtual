import os
import tempfile
import streamlit as st
import re # Importa re para as funções de formatação
# Importa as funções do módulo core.core_correction
from core.core_correction import corecao_redacao, verificar_sentido_redacao_com_arquivo

def formatar_resultado(resultado_redacao: str, vestibular: str):
    """
    Exibe o resultado da correção da redação no Streamlit com base no vestibular,
    garantindo que notas e justificativas sejam exibidas.
    """
    vestibular = vestibular.upper()

    if vestibular == "ENEM":
        # Busca e exibe a nota total da redação
        nota_total_match = re.search(r"Nota final:.*", resultado_redacao, re.IGNORECASE)
        if nota_total_match:
            st.markdown(f"### {nota_total_match.group()}")

        # Extrai os trechos de cada competência, incluindo a justificativa
        blocos_competencias = re.findall(
            r"(\*\*Competência \d[\s\S]*?Nota:.*?[\s\S]*?(?=\n\*\*Competência|\Z))",
            resultado_redacao,
            re.MULTILINE
        )

        # Exibe cada competência em um container separado
        for bloco in blocos_competencias:
            with st.container():
                st.markdown(bloco.strip())

    elif vestibular == "UNICAMP":
        nota_total_match = re.search(r"Nota final:.*", resultado_redacao, re.IGNORECASE)
        if nota_total_match:
            st.markdown(f"### {nota_total_match.group()}")

        # Captura os critérios com suas notas e justificativas
        blocos_criterios = re.findall(
            r"(\*\*Critério \d[\s\S]*?Nota:.*?[\s\S]*?(?=\n\*\*Critério|\Z))",
            resultado_redacao
        )

        for bloco in blocos_criterios:
            with st.container():
                st.markdown(bloco.strip())

    elif vestibular == "FUVEST":
        nota_match = re.search(r"Nota final:.*", resultado_redacao, re.IGNORECASE)
        if nota_match:
            st.markdown(f"### {nota_match.group()}")

        # Isola a justificativa após a nota.
        partes = resultado_redacao.split("Nota final:")
        if len(partes) > 1:
            justificativa = partes[1].strip()
            # A linha que removia um possível número inicial foi removida para garantir
            # que a justificativa completa seja exibida.
            if justificativa:
                with st.container():
                    st.markdown(justificativa)
    elif vestibular == "UECE":
        # Busca e exibe a nota total da redação
        nota_total_match = re.search(r"Nota final:.*", resultado_redacao, re.IGNORECASE)
        if nota_total_match:
            st.markdown(f"### {nota_total_match.group()}")

        # Extrai os trechos de cada competência, incluindo a justificativa
        blocos_competencias = re.findall(
            r"(\*\*.*?\*\*\s*Nota: \d+[\s\S]+?)(?=\n\*\*|\Z)",
            resultado_redacao,
            re.MULTILINE
        )

        # Exibe cada competência em um container separado
        for bloco in blocos_competencias:
            with st.container():
                st.markdown(bloco.strip())

    else:
        st.error("Vestibular não suportado para exibição dos resultados.")


# --- Interface do Usuário Streamlit ---
st.markdown("<h1 style='color: #d39eff;'>Correção de Redação</h1>", unsafe_allow_html=True)
st.markdown("Escolha se deseja digitar a redação ou enviar um arquivo. Depois, selecione o vestibular, o tema e receba uma correção detalhada.")
#st.markdown("#### Como funciona a correção da redação de cada vestibular?")
#st.markdown("[Correção Enem](https://www.cnnbrasil.com.br/educacao/redacao-do-enem-perguntas-e-respostas-sobre-a-correcao/), [Correção Fuvest (USP)](https://www.cnnbrasil.com.br/educacao/redacao-da-fuvest-2025-saiba-como-e-feita-a-correcao/), [Correção Unicamp](https://querobolsa.com.br/revista/como-e-a-correcao-da-redacao-da-unicamp)", unsafe_allow_html=True)

st.divider()

modo = st.selectbox("Metodo de envio da redação", ["", "Escrever texto", "Enviar arquivo"])

texto_redacao = None
arquivo = None

if modo == "Escrever texto":
    texto_redacao = st.text_area("Digite sua redação aqui:", height=300)

elif modo == "Enviar arquivo":
    arquivo = st.file_uploader(
        "Envie sua redação (PDF, imagem, DOCX ou TXT)",
        type=["pdf", "png", "jpg", "jpeg", "webp", "txt", "docx"]
    )

tema = st.text_input("Escreva o tema")
vestibular = st.selectbox("Selecione o vestibular para correção:", ["", "ENEM", "FUVEST", "UNICAMP", "UECE"])

if st.button("Corrigir redação", type="primary"):
    if not vestibular:
        st.warning("Selecione o vestibular.")
    elif not tema:
        st.warning("Informe o tema da redação.")
    elif modo == "Escrever texto" and not texto_redacao:
        st.warning("Digite sua redação.")
    elif modo == "Enviar arquivo" and not arquivo:
        st.warning("Envie um arquivo.")
    else:
        with st.spinner("Corrigindo a redação..."):
            temp_path = None
            try:
                if modo == "Escrever texto":
                    if len(texto_redacao.strip()) < 1000:
                        st.error("Por favor, envie uma redação com pelo menos 1000 caracteres.")
                    else:
                        # Cria um arquivo temporário para a entrada de texto
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp_file:
                            tmp_file.write(texto_redacao)
                            temp_path = tmp_file.name
                        
                        # Verifica o conteúdo antes da correção
                        if not verificar_sentido_redacao_com_arquivo(temp_path, tema):
                            st.error("O conteúdo da redação digitada não parece ser uma redação válida sobre o tema proposto.")
                        else:
                            resultado = corecao_redacao(vestibular=vestibular, tema=tema, file_path=temp_path)
                            formatar_resultado(resultado, vestibular)
                else: # modo == "Enviar arquivo"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(arquivo.name)[1]) as tmp_file:
                        tmp_file.write(arquivo.getbuffer())
                        temp_path = tmp_file.name

                    if not verificar_sentido_redacao_com_arquivo(temp_path, tema):
                        st.error("O conteúdo do arquivo enviado não parece ser uma redação válida sobre o tema proposto.")
                    else:
                        resultado = corecao_redacao(vestibular=vestibular, tema=tema, file_path=temp_path)
                        formatar_resultado(resultado, vestibular)
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)
