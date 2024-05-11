import streamlit as st
from backend import Ia

chat = Ia()

class MeuApp:
    
    def __init__(self) -> None:
        st.title("Chat")
        
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
