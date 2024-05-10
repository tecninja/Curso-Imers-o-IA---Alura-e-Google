import google.generativeai as genai
import streamlit as st
import boto3
import os

API_KEY = st.secrets['gemini_token']
os.environ['Access key ID'] = st.secrets['AWS_ACCESS_KEY_ID']
os.environ['Secret access key'] = st.secrets['AWS_SECRET_ACCESS_KEY']
os.environ['region'] = st.secrets['AWS_DEFAULT_REGION']


class Ia:
    
    def __init__(self) -> None:
        pass
    
    
class Nuvem:
    
    BUCKET = "exms-treino-primeiro-bucket"
    
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
    

    def enviar_objeto(self, obj, obj_name):
        
        try:
            self.s3.Bucket(self.BUCKET).put_object(Key=obj_name, Body=obj)
        except Exception as e:
            return {"status":False,
                    "contexto": f"Erro no envio do arquivo {obj_name}: {e}"}
        else:
            return {"status":True,
                    "contexto": f"Arquivo {obj_name} enviado com sucesso"}
        
    def listar_objetos(self):
        try:
            bkt = self.s3.Bucket(self.BUCKET)
            objetos = [obj.key for obj in bkt.objects.all()]
        except Exception as e:
            return {"status":False,
                    "contexto":f"Erro na busca - {e}"}
        else:
            return {"status":True,
                    "contexto":"Objetos listados com sucesso",
                    "objetos":objetos}
    
    def apagar_objetos(self, obj_name):
        try:
            self.s3.Object(self.BUCKET, obj_name).delete()
        except Exception as e:
            return {"status":False,
                    "contexto": f"Erro ao apagar arquivo {obj_name}. Detalhamento: {e}"}
        else:
            return {"status":True,
                    "contexto": f"Arquivo {obj_name} apagado com sucesso"
                    }