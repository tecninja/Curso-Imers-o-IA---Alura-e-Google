import streamlit as st
from backend import Nuvem

class Cadastro:

    def __init__(self) -> None:
        st.title("Cadastre Documentos de Contexto")
        
        
        with st.expander("Cadastro"):
            file = st.file_uploader(
                "Selecione o arquivo",
                accept_multiple_files=True
                )
            
            if st.button("Enviar Arquivo"):
                if file:
                    for item in file:
                        resposta = Nuvem().enviar_objeto(
                            obj=item.getvalue(),
                            obj_name=item.name
                            )
                        if resposta["status"]:
                            st.success(resposta['contexto'])
                        else:
                            st.error(resposta['contexto'])
                else:
                    st.error("Nenhum arquivo selecionado")
                
        with st.expander("Exclusão"):
            resposta = Nuvem().listar_objetos()
            if resposta['status']:
                selecao = st.radio(
                    label="Escolha qual arquivo excluir",
                    options=resposta['objetos']
                )
                
                if st.button("Apagar Arquivo"):
                    resposta = Nuvem().apagar_objetos(selecao)
                    if resposta['status']:
                        st.success(resposta['contexto'])
                    else:
                        st.error(resposta['contexto'])    
            else:
                st.error(f"Erro ao buscar objetos: {resposta['contexto']}")

Cadastro()
