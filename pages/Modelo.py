import streamlit as st
from backend import *

class Modelo:

    def __init__(self) -> None:
        if "objetos_contexto" not in st.session_state:
            st.session_state.objetos_contexto = []
            
        st.title("Selecione o Modelo de IA a ser utilizado")
                
        if "api_key" not in st.session_state or \
            st.session_state.api_key == "":
            st.toast("Informe uma api_key para prosseguir")
            st.write("Informe sua api key na aba\
                <a href='/' target='_self'>chat</a>",
                unsafe_allow_html=True)
        else:
            modelos = [model.name for model in Ia().pegar_modelos()]
            
            if "modelo_selecionado" not in st.session_state:
                st.session_state.modelo_selecionado = [None,None]
            
            modelo = st.radio(label="Modelos",
                    options=modelos,
                    index=st.session_state.modelo_selecionado[0])
            
            st.session_state.modelo_selecionado = [modelos.index(modelo),modelo] 

Modelo()
