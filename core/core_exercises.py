import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

gemini_api = os.getenv("GEMINI_API_KEY")

if gemini_api:
    genai.configure(api_key=gemini_api)
else:
    st.error("Chave de API do Google não encontrada.")
    st.stop() 

def gerar_exercicio(topico, nivel):
    try:
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
    
    except Exception as e:
        print(f"error no núcleo do exercicio: {e}")
        return[]
        
        
        
        
        