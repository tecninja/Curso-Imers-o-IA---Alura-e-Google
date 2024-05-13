import google.generativeai as genai
import streamlit as st
# import boto3
# import os
import pandas as pd
import io
from PyPDF2 import PdfReader
import codecs
from unidecode import unidecode
import fitz
# As linhas a baixo maximizam a funcionalidade para o seu uso de maneira escalável
# deixando o sistema independente da imposição da chave api em toda sessão, além
# de guardar os objetos de contexto em nuvem da aws

#API_KEY = st.secrets['gemini_token']
# os.environ['Access key ID'] = st.secrets['AWS_ACCESS_KEY_ID']
# os.environ['Secret access key'] = st.secrets['AWS_SECRET_ACCESS_KEY']
# os.environ['region'] = st.secrets['AWS_DEFAULT_REGION']


class Ia:
    
    def __init__(self) -> None:
        API_KEY = st.session_state.api_key
        genai.configure(api_key=API_KEY)
        
        if "modelo_selecionado" not in st.session_state:
            st.session_state.modelo_selecionado = [0,"gemini-1.0-pro"]
        
        model_name = st.session_state.modelo_selecionado[1]
        
        model = genai.GenerativeModel(model_name=model_name)
        
        if "history" not in st.session_state:
            st.session_state.history = []
        self.chat = model.start_chat(history=st.session_state.history)
        
        # if "arquivos_contexto" not in st.session_state:
        #     st.session_state.arquivos_contexto = Nuvem().pegar_objetos()["objeto"]
        
        self.contexto = []
        
        for item in st.session_state.objetos_contexto:
            # [ ]
            if item['item_name'].__contains__("csv"):
                csv_buffer = io.BytesIO(item['item_content'])
                df = pd.read_csv(csv_buffer)
                self.contexto.append(df)
                
            if item['item_name'].__contains__("txt"):
                with io.BytesIO(item['item_content']) as arquivo:
                    texto = arquivo.read().decode(encoding="utf-8", errors='ignore')
                self.contexto.append(texto)
            
            if item['item_name'].__contains__("pdf"):
                arquivo = io.BytesIO(item['item_content'])
                with fitz.open(stream=arquivo.read(), filetype='pdf') as doc:
                    texto_completo = ""
                    for page in doc:
                        texto_completo += page.get_textpage().extractText()
                    
                self.contexto.append(texto_completo)
                
    def gerar_resposta(self, prompt):
        
        if self.contexto == []:
            prompt_final = prompt
        else:
            prompt_final = f"""
            Responda a seguinte prompt: {prompt} 
            Porém sua única fonte de dados deve ser os\
            seguintes arquivos de contexto: {self.contexto}
            """
        try:
            response = self.chat.send_message(prompt_final)
            for parts in self.chat.history:
                st.session_state.history.append(parts)
            return response.text
        except Exception as e:
            return f"Desculpe houve um erro: {e}\nVerifique\
                se suas credenciais de API Key foram passadas corretamente"
            
    
    def pegar_modelos(self):
        modelos = genai.list_models()
        return modelos
    
class Nuvem:
    
    BUCKET = "exms-treino-primeiro-bucket"
    
    def __init__(self) -> None:
        #self.s3 = boto3.resource("s3")
        ...

    def pegar_objetos(self):
        try:
            # arquivos_de_contexto = []
            # objetos = self.listar_objetos()["objetos"]
            # objetos = st.session_state.objetos_contexto
            # for item in objetos:

                # obj = self.s3.Object(self.BUCKET, item)
                # obj_content = obj.get()['Body'].read()

                # arquivos_de_contexto.append({
                    # "item_name":item['nome'],
                    # "item_content":item['conteudo']
                    # }
                                            # )
            pass
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
                "objeto": st.session_state.objetos_contexto
            }
            

    def enviar_objeto(self, obj, obj_name):
        
        try:
            # Usar a linha a baixo para subir aquivo num bucket s3
            # self.s3.Bucket(self.BUCKET).put_object(Key=obj_name, Body=obj)
            
            st.session_state.objetos_contexto.append({
                "item_name": obj_name,
                "item_content":obj
                    })
        except Exception as e:
            return {"status":False,
                    "contexto": f"Erro no envio do arquivo {obj_name}: {e}"}
        else:
            return {"status":True,
                    "contexto": f"Arquivo {obj_name} enviado com sucesso"}
   
    # Depreciada - Essa função faz sentido no uso do S3 da AWS
    def listar_objetos(self):
        """Depreciada
        """
        try:
            # Usar a linha a baixo para subir aquivo num bucket s3
            # bkt = self.s3.Bucket(self.BUCKET)
            # objetos = [obj.key for obj in bkt.objects.all()]
            
            lista_objetos = st.session_state.objetos_contexto
        except Exception as e:
            return {"status":False,
                    "contexto":f"Erro na busca - {e}"}
        else:
            return {"status":True,
                    "contexto":"Objetos listados com sucesso",
                    "objetos":lista_objetos}
    
    def apagar_objetos(self, obj_name):
        try:
            # Usar a linha a baixo para subir aquivo num bucket s3
            # self.s3.Object(self.BUCKET, obj_name).delete()
            
            for o in st.session_state.objetos_contexto:
                if o['item_name'] == obj_name:
                    st.session_state.objetos_contexto.remove(o)
                    
        except Exception as e:
            return {"status":False,
                    "contexto": f"Erro ao apagar arquivo {obj_name}. Detalhamento: {e}"}
        else:
            return {"status":True,
                    "contexto": f"Arquivo {obj_name} apagado com sucesso"
                    }
