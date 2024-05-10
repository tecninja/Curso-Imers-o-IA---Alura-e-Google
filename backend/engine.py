import google.generativeai as genai
import streamlit as st
import boto3
import os

API_KEY = st.secrets['gemini_token']
os.environ['Access key ID'] = st.secrets['Access_key_ID']
os.environ['Secret access key'] = st.secrets['Secret_access_key']
os.environ['region'] = st.secrets['region']


class Ia:
    
    def __init__(self) -> None:
        pass
    
    
class Nuvem:
    
    
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
    

    def enviar_objeto(self, obj, obj_name):
        try:
            self.s3.Bucket("exms-treino-primeiro-bucket").put_object(Key=obj_name, Body=obj)
        except Exception as e:
            return {"status":False, "contexto": f"Erro no envio: {e}"}
        else:
            return {"status":True, "contexto": "Arquivo enviado com sucesso"}
            
            