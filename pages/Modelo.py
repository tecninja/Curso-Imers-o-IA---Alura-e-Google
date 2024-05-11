import streamlit as st
from backend import *

class Modelo:

    def __init__(self) -> None:
        if "obejetos_contexto" not in st.session_state:
            st.session_state.objetos_contexto = []
            
        st.title("Selecione o Modelo de IA a ser utilizado")
        
        with st.sidebar:
            st.subheader("Informe sua API KEY do Gemini")
            st.session_state.api_key = st.text_input("Api Key", type="password")
            st.warning("Você precisa forcer uma chave de api válida para usar o sistema")
        
        if "api_key" not in st.session_state or \
            st.session_state.api_key == "":
            st.toast("Informe uma api_key para prosseguir")
        else:
            modelos = [model.name for model in Ia().pegar_modelos()]
            
            if "modelo_selecionado" not in st.session_state:
                st.session_state.modelo_selecionado = [None,None]
            
            modelo = st.radio(label="Modelos",
                    options=modelos,
                    index=st.session_state.modelo_selecionado[0])
            
            st.session_state.modelo_selecionado = [modelos.index(modelo),modelo] 

Modelo()
