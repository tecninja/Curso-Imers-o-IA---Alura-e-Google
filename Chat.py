import streamlit as st
from backend import Ia



class MeuApp:
    
    def __init__(self) -> None:
        if "objetos_contexto" not in st.session_state:
            st.session_state.objetos_contexto = []    
        st.title("Asistente de Trabalho")
        st.divider()
        st.write("Para usar o assitente de trabalho, você deve ter uma \
            api key do gemini válida, e deve a inserir no campo específico\
            do menu ao lado.\
            Você pode testar modelos diferentes do Gemini usando acessando a\
            aba <a href='/Modelo' target='_self'>Modelo</a>, além de poder\
            cadastrar objetos do tipo texto para dar contexto ao seu assistente\
            na aba <a href='/Cadastro_de_Contexto' target='_self'>Cadastro de Contexto</a>.",
                        unsafe_allow_html=True)
        
        with st.sidebar:
            st.subheader("Informe sua API KEY do Gemini")
            if "api_key" in st.session_state:
                API_KEY = st.text_input("Api Key",
                                        type="password",
                                        value=st.session_state.api_key
                                        )
                st.session_state.api_key = API_KEY
                st.warning("Você precisa forcer uma chave de api válida para usar o sistema")
            else:
                API_KEY = st.text_input("Api Key",
                                        type="password",
                                        )
                st.session_state.api_key = API_KEY
                st.warning("Você precisa forcer uma chave de api válida para usar o sistema")
        
        if "api_key" not in st.session_state or \
            st.session_state.api_key == "":
            st.toast("Informe uma api_key para prosseguir")
        else:
            chat = Ia()
            if "messages" not in st.session_state:
                st.session_state["messages"] = [{"role": "assistant", "content": "Oi, como eu posso te ajudar?"}]

            
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])
            
            if prompt := st.chat_input():
                
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                
                response = chat.gerar_resposta(prompt=prompt)
                
                msg = response
                
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.chat_message("assistant").write(msg)

MeuApp()
