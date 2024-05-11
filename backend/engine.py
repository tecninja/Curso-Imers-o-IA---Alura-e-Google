import google.generativeai as genai
import streamlit as st
import boto3
import os
import pandas as pd
import io

API_KEY = st.secrets['gemini_token']
os.environ['Access key ID'] = st.secrets['AWS_ACCESS_KEY_ID']
os.environ['Secret access key'] = st.secrets['AWS_SECRET_ACCESS_KEY']
os.environ['region'] = st.secrets['AWS_DEFAULT_REGION']


class Ia:
    
    def __init__(self) -> None:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.0-pro")
        if "history" not in st.session_state:
            st.session_state.history = []
        self.chat = model.start_chat(history=st.session_state.history)
        
        if "arquivos_contexto" not in st.session_state:
            st.session_state.arquivos_contexto = Nuvem().pegar_objetos()["objeto"]
        
        self.contexto = []
        
        for item in st.session_state.arquivos_contexto:
            
            if item['item_name'].__contains__("csv"):
                csv_buffer = io.BytesIO(item['item_content'])
                df = pd.read_csv(csv_buffer)
                self.contexto.append(df)
                


    def gerar_resposta(self, prompt):
        
        prompt_final = f"""
        Responda a seguinte prompt: {prompt} 
        Porém sua única fonte de dados deve ser os seguintes arquivos de contexto: {self.contexto}
        """
        
        response = self.chat.send_message(prompt_final)
        for parts in self.chat.history:
            st.session_state.history.append(parts)
        return response.text
    
class Nuvem:
    
    BUCKET = "exms-treino-primeiro-bucket"
    
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
        

    def pegar_objetos(self):
        try:
            arquivos_de_contexto = []
            objetos = self.listar_objetos()["objetos"]
            for item in objetos:
                obj = self.s3.Object(self.BUCKET, item)
                obj_content = obj.get()['Body'].read()
                arquivos_de_contexto.append({
                    "item_name":item,
                    "item_content":obj_content
                    }
                                            )
        except Exception as e:
            return {
                "status":False,
                "contexto":f"Erro ao baixar arquivos de contexto. Detalhamento: {e}",
                "objeto": []
            }
        else:
            return {
                "status":True,
                "contexto":"Sucesso no download dos arquivos de contexto",
                "objeto": arquivos_de_contexto
            }
            

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
