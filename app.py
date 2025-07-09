import streamlit as st

st.set_page_config(
    page_title="App Escolar IA",
    page_icon="🎓",
    layout="wide"
)

pages = {
    "Navegação":[
        st.Page("./pages/home.py", title="Home", icon="🏠"),
        st.Page("./pages/exercises.py", title="Exercises", icon="🧠")  
    ],
}

pg = st.navigation(pages)
pg.run()