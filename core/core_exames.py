import streamlit as st
from constants.exames_constants import enem_tests, fuvest_tests, unicamp_tests, uece_tests

def botao_link(prova_url, gabarito_url, prova_label="Prova", gabarito_label="Gabarito"):
    btn1, btn2 = st.columns(2)
    with btn1:
        st.link_button(prova_label, prova_url, use_container_width=True, type="primary", icon="📓")
    with btn2:
        st.link_button(gabarito_label, gabarito_url, use_container_width=True, type="secondary", icon="📒")

def ENEM():
    for ano, data in enem_tests.items():
        with st.expander(f"ENEM - Prova {ano}", expanded=False):
            for dia, info in data.items():
                st.markdown(f"### {dia}")
                botao_link(info["Prova"], info["Gabarito"])
           
def UECE():
    for ano, data in uece_tests.items():
        with st.expander(f"UECE - Prova {ano}", expanded=False):
            for dia, info in data.items():
                st.markdown(f"### {dia}")
                botao_link(info["Prova"], info["Gabarito"])

def FUVEST():
    for ano, data in fuvest_tests.items():
        with st.expander(f"FUVEST - Prova {ano}", expanded=False):
            for fase, info in data.items():
                if "Prova" in info and "Gabarito" in info:
                    st.markdown(f"### {fase}")
                    botao_link(info["Prova"], info["Gabarito"])
                elif fase == "Segunda Fase":
                    st.markdown("""----------""")
                    st.markdown("""### Segunda Fase""")
                    
                    for dia, detalhes in info.items():
                        if "Prova" in detalhes and "Gabarito" in detalhes:
                            st.markdown(f"#### {dia}")
                            
                            botao_link(detalhes["Prova"], detalhes["Gabarito"])

def UNICAMP():
    for ano, data in unicamp_tests.items():
        with st.expander(f"UNICAMP - Prova {ano}", expanded=False):
            # Primeira Fase
            if "Primeira Fase" in data:
                st.markdown("### Primeira Fase")
                botao_link(
                    data["Primeira Fase"]["Prova"],
                    data["Primeira Fase"]["Gabarito"]
                )

            # Segunda Fase - Dia 1
            if "Segunda Fase" in data:
                fase2 = data["Segunda Fase"]
                st.markdown("### Segunda Fase - Dia 1")
                botao_link(
                    fase2["Dia 1"]["Prova"],
                    fase2["Dia 1"]["Gabarito"],
                )

                # Segunda Fase - Dia 2
                st.markdown("### Segunda Fase - Dia 2")
                for area in ["Biológia", "Exatas", "Humanas"]:
                    botao_link(
                        fase2["Dia 2"][area]["Prova"],
                        fase2["Dia 2"][area]["Gabarito"],
                        prova_label=f"Prova de {area}",  # Modified here
                        gabarito_label=f"Gabarito de {area}" # Modified here
                    )