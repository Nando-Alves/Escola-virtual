import streamlit as st
from core import core_exames
st.title("📒 Estude para seu vestibular através de provas já realizadas")
st.markdown("""
Escolha um vestibular
---""")
tab_enem, tab_uece, tab_fuvest, tab_unicamp = st.tabs(["ENEM", "UECE","FUVEST","UNICAMP"])

with tab_enem:
    core_exames.ENEM()

with tab_uece:
    core_exames.UECE()

with tab_fuvest:
    core_exames.FUVEST()

with tab_unicamp:
    core_exames.UNICAMP()