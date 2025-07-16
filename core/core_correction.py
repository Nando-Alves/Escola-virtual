import os
import google.generativeai as genai
from mimetypes import guess_type
import re
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (assumindo que um arquivo .env existe com GEMINI_API_KEY)
load_dotenv()

# Configura a API Generative AI com a chave de API
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

def criterios_redacao(vestibular):
    """
    Retorna os critérios de avaliação para um determinado vestibular (ENEM, UNICAMP, FUVEST).
    """
    vestibular = vestibular.upper()
    if vestibular == 'ENEM':
        return {
            'criterios': """
Corrija a redação com base nos **critérios oficiais do ENEM**, avaliando as 5 competências exigidas:

---

🔹 **Competência 1 – Domínio da norma padrão da língua portuguesa**
Avalie se o texto segue as regras gramaticais, ortográficas, de pontuação e concordância da modalidade escrita formal da língua portuguesa.

🔹 **Competência 2 – Compreensão da proposta de redação**
Verifique se o participante compreendeu o tema proposto e conseguiu desenvolver um **texto dissertativo-argumentativo** dentro do contexto exigido.

🔹 **Competência 3 – Seleção e organização de argumentos**
Analise a capacidade de selecionar, organizar e relacionar **informações, fatos e opiniões** para defender um ponto de vista com **coerência e progressão temática**.

🔹 **Competência 4 – Coesão e coerência na argumentação**
Considere o uso de **recursos linguísticos**, como conectivos, pronomes e operadores argumentativos, para articular as ideias de forma **clara e lógica** ao longo do texto.

🔹 **Competência 5 – Proposta de intervenção**
Avalie se há uma **proposta de intervenção** que enfrente o problema discutido no texto, apresentando ações detalhadas (agente, ação, meio, efeito) e que **respeite os direitos humanos**.


---""",
            'nota_enem': "A pontuação total da redação do ENEM é de 0 a 1000 pontos.",
            'instrucao_pontuacao': "Forneça uma pontuação para cada competência de 0 a 200 e uma pontuação total."
        }
    elif vestibular == 'UNICAMP':
        return {
            'criterios': """
Corrija a redação com base nos **critérios de avaliação da UNICAMP**, atribuindo nota parcial a cada um dos seguintes aspectos:

🔹 **1. Compreensão da proposta temática (até 2 pontos)**
🔹 **2. Adequação ao gênero solicitado (até 3 pontos)**
🔹 **3. Leitura e uso dos textos de apoio (até 3 pontos)**
🔹 **4. Convenções da escrita e coesão textual (até 4 pontos)**""",
            'pontuacao': "A pontuação total da redação da UNICAMP varia de 0 a 12 pontos.",
            'instrucao_pontuacao': "Atribua uma pontuação para cada critério acima e forneça a pontuação total ao final."
        }
    elif vestibular == 'FUVEST':
        return {
            'criterios': """
Corrija a redação com base nos **critérios de avaliação da FUVEST**:

🔹 Desenvolvimento consistente do tema
🔹 Argumentação coerente
🔹 Domínio da norma culta da língua portuguesa""",
            'pontuacao': "A pontuação total da redação da FUVEST varia de 0 a 50 pontos.",
            'instrucao_pontuacao': "Atribua uma pontuação geral (0 a 50 pontos), com uma justificativa técnica para a nota."
        }
    elif vestibular == 'UECE':
        return {
        'criterios': """
Corrija a redação com base nos **critérios oficiais da UECE**, considerando os seguintes aspectos:

---

🔹 **Estrutura e organização textual**
Verifique se o texto apresenta introdução, desenvolvimento e conclusão de forma articulada, clara e bem delimitada.

🔹 **Argumentação e conteúdo**
Avalie a capacidade de apresentar um ponto de vista e desenvolvê-lo com argumentos relevantes, consistentes e adequados ao tema proposto.

🔹 **Coesão e coerência**
Considere a lógica e clareza na progressão das ideias, observando o uso apropriado de conectivos, pronomes e outros mecanismos linguísticos de articulação textual.

🔹 **Domínio da norma culta da língua**
Observe a correção gramatical, ortográfica, de pontuação, concordância e regência, além do uso adequado do vocabulário formal.

---
""",
        'nota_uece': "A pontuação total da redação da UECE varia de 0 a 100 pontos.",
        'instrucao_pontuacao': "Forneça uma nota de 0 a 25 para cada critério e a pontuação total."
    }

    else:
        raise ValueError("Vestibular inválido.")

def verificar_sentido_redacao_com_arquivo(file_path, tema):
    """
    Verifica se o conteúdo de um arquivo (redação) é coerente com o tema fornecido.
    Usa Gemini-1.5-flash para análise de conteúdo.
    """
    try:
        mime_type, _ = guess_type(file_path)
        with open(file_path, "rb") as f:
            media = {
                "mime_type": mime_type,
                "data": f.read()
            }

        prompt = f"""
            Você receberá o conteúdo de um arquivo que pode conter uma redação.

            Analise o texto considerando os seguintes pontos:

            1. A redação apresenta uma estrutura textual coerente, composta por:
            - Introdução (apresentação do tema);
            - Desenvolvimento (argumentação);
            - Conclusão (fechamento das ideias).

            2. O conteúdo está relacionado ao tema abaixo:
            Tema: "{tema}"

            Apenas responda com **SIM** ou **NÃO**. Não inclua explicações.
            """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, media])
        return "SIM" in response.text.upper()
    except Exception as e:
        print(f"Erro ao verificar sentido da redação: {e}")
        return False

def corecao_redacao(vestibular, tema, file_path):
    """
    Corrige uma redação com base nos critérios do vestibular especificado usando Gemini-1.5-flash.
    O conteúdo da redação é lido do file_path fornecido.
    """
    try:
        vestibular = vestibular.upper()
        pegar_criterios = criterios_redacao(vestibular)

        corpo_prompt = ""
        if vestibular == "ENEM":
            corpo_prompt = """
            Você é um corretor especializado do vestibular {vestibular}.

            ⚠️ Tudo que estiver entre colchetes NÃO deve ser impresso. São apenas instruções para você.

            Corrija a redação enviada com base nos critérios abaixo, avaliando de forma técnica e estruturada.

            📌 Tema da redação: "{tema}"
            **VALE RESALTA QUE CASO A REDAÇÂO FUJA DO TEMA ELA DEVE SER ZERADA**

            {criterios}
            {nota_enem}
            {instrucao_pontuacao}

            ---

            ✍️ Formato obrigatório da resposta:
            
            - Nota final: [nota total]

            (Para vestibulares com competências ou critérios separados, apresente cada item no padrão abaixo:)

            **[Nome da competência ou critério]**
            Nota: [valor atribuído]
            [Justificativa técnica da nota]

            ❌ Não inclua sugestões, conselhos, elogios ou reescritas. Apenas a correção técnica e objetiva.
            """.format(tema=tema, vestibular=vestibular, **pegar_criterios)

        elif vestibular == "UNICAMP":
            corpo_prompt = """
            Você é um corretor especializado da banca avaliadora da UNICAMP.

            ⚠️ Tudo que estiver entre colchetes NÃO deve ser impresso. São apenas instruções para você.

            Corrija a redação com base nos critérios da UNICAMP, avaliando os 4 aspectos descritos abaixo com clareza, objetividade e rigor técnico.

            📌 Tema da redação: "{tema}"
            **VALE RESALTA QUE CASO A REDAÇÂO FUJA DO TEMA ELA DEVE SER ZERADA**
            {criterios}
            {pontuacao}
            {instrucao_pontuacao}

            ---

            ✍️ **Formato obrigatório da resposta:**

            - Nota final: [nota total de 0 a 12]

            - **Critério 1 – Compreensão da proposta temática**
            Nota: [0 a 2]
            [Justificativa técnica clara, baseada na relevância e adequação ao tema]

            - **Critério 2 – Adequação ao gênero solicitado**
            Nota: [0 a 3]
            [Justificativa baseada na fidelidade ao gênero textual exigido]

            - **Critério 3 – Leitura pertinente dos textos de apoio**
            Nota: [0 a 3]
            [Justificativa sobre como os textos foram usados de forma crítica e integrada]

            - **Critério 4 – Convenções da escrita e coesão textual**
            Nota: [0 a 4]
            [Justificativa com base na correção gramatical, ortográfica e na coesão textual]

            ❌ Não forneça sugestões, conselhos ou reescritas. Apenas a correção técnica conforme o padrão acima
            """.format(tema=tema, **pegar_criterios)

        elif vestibular == "FUVEST":
            corpo_prompt = """
            Você é um corretor especializado da banca da FUVEST.

            ⚠️ Tudo que estiver entre colchetes NÃO deve ser impresso. São apenas instruções para você.

            Corrija a redação com base nos critérios oficiais da FUVEST, avaliando o desempenho geral do(a) candidato(a) conforme os três aspectos abaixo:

            - Desenvolvimento consistente do tema
            - Argumentação coerente
            - Domínio da norma culta da língua portuguesa

            📌 Tema da redação: "{tema}"
            **VALE RESALTA QUE CASO A REDAÇÂO FUJA DO TEMA ELA DEVE SER ZERADA**
            {criterios}
            {pontuacao}
            {instrucao_pontuacao}

            ---

            ✍️ **Formato obrigatório da resposta:**

            - Nota final: [nota de 0 a 50]

            [Justificativa técnica única, objetiva e coesa, baseada nos três critérios acima. Aponte pontos fortes e/ou limitações da redação com clareza, sem sugestões.]

            ❌ Não forneça conselhos, elogios, reescritas ou observações adicionais. Apenas a correção técnica conforme o padrão exigido.
            """.format(tema=tema, **pegar_criterios)
        elif vestibular == "UECE":
             corpo_prompt = """
    Você é um corretor especializado do vestibular {vestibular}.

    ⚠️ Tudo que estiver entre colchetes NÃO deve ser impresso. São apenas instruções para você.

    Corrija a redação enviada com base nos critérios abaixo, avaliando de forma técnica e estruturada.

    📌 Tema da redação: "{tema}"
    **VALE RESSALTAR QUE, CASO A REDAÇÃO FUJA TOTALMENTE DO TEMA, ELA DEVE SER ZERADA.**

    {criterios}
    {nota_uece}
    {instrucao_pontuacao}

    ---

    ✍️ Formato obrigatório da resposta:
    
    - Nota final: [nota total]

    **[Nome do critério]**
    Nota: [valor atribuído]
    [Justificativa técnica da nota]

    ❌ Não inclua sugestões, conselhos, elogios ou reescritas. Apenas a correção técnica e objetiva.
    """.format(tema=tema, vestibular=vestibular, **pegar_criterios)
        else:
            raise ValueError("Vestibular inválido.")

        # Lê o conteúdo do arquivo
        mime_type, _ = guess_type(file_path)
        with open(file_path, "rb") as f:
            media = {
                "mime_type": mime_type,
                "data": f.read()
            }

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([corpo_prompt, media])
        return response.text.strip()

    except Exception as e:
        return f"Erro de correção: {e}"
