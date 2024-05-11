import streamlit as st
from backend import Nuvem

class Cadastro:

    def __init__(self) -> None:
        if "obejetos_contexto" not in st.session_state:
            st.session_state.objetos_contexto = []
        st.title("Cadastre Documentos de Contexto")
        
        
        with st.expander("Cadastro"):
            file = st.file_uploader(
                "Selecione o arquivo",
                accept_multiple_files=True,
                type=["txt","csv","xlsx","pdf"]
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
                resposta = [obj['nome'] for obj in resposta['objetos']]
                selecao = st.radio(
                    label="Escolha qual arquivo excluir",
                    options=resposta
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
