import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api = os.getenv("GEMINI_API_KEY")

if gemini_api:
    genai.configure(api_key=gemini_api)
else:
    st.error("Chave de API do Google não encontrada.")
    st.stop()

def gerar_resumo(topico):
    try:
        prompt = f"""Formate a resposta da seguinte maneira:

        # :blue[{topico}]
    
        Crie um resumo claro e objetivo para vestibulandos sobre o tema '{topico}'.
        O resumo deve conter informações relevantes e ser de fácil compreensão.

        Organize o resumo com títulos bem definidos, por exemplo:

        ## :blue[Título do tema]
        Texto do resumo, de forma clara e concisa, focado para vestibular.
        
        Ao fim coloque "como tal assunto é cobrado nos vestibulares".
        
        Não coloque "dicas ou algo do tipo", apenas o resumo."""
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"error ao gerar resumo: {e}")
        return"Não foi possível gerar o resumo no momento."