import pymongo
import re
import datetime
import sys
from bson import ObjectId
import os

class DB:

    def _init_(self):
        self.con = None
        self.var_ID_exist_conversacion= None
        self.var_check_last_conversacion= None
        self.var_ID_crear_conversacion=None
        self.var_check_message_unsend=None
        self.var_check_last_message_in= None
        self.var_check_lasts_message_in_db=None
        self.var_check_last_photo_in=None
        self.var_update_state_msg_unsend=None
        self.var_check_lasts_photo_in=None
        self.con_monitoreo=None
        self.var_check_last_conversacion_id=None
        self.var_check_lasts_video_in = None
        self.var_check_lasts_docs_in = None
        self.var_check_lasts_audio_in = None
        self.var_check_file_unsend = None
        self.var_check_conversaciones_inactivos = None
        self.var_check_chats_espera = None


    def conect(self):
        #DB = "iContactdb"
        #URL_DB = ""
        client = pymongo.MongoClient(os.environ.get("string_mongo"))
        db = client[os.environ.get("db")]
        self.con = db

    def get_trace_itents(self,conversacion):
        try:
            print("### get_trace_itents ###")
            db = self.con
            col = db['conversaciones']

            query = {"_id":ObjectId(conversacion)}
      
            result = col.find_one(query,{"name_itent":1})

            var_name_itent = result.get('name_itent', ["0"])

            return var_name_itent
       
        except:
            print(sys.exc_info())

    def get_config(self,api):
        db = self.con
        col = db['apis']

        query = {"API":api}

        result = col.find_one(query,{"url":1,"token":1,"token_wompi":1,"token_catalogo":1,"url_catalogo":1}) 
        
        if col.count_documents(query) != 0:
            return result['url'],result['token'],result['token_wompi'],result['token_catalogo'],result['url_catalogo']
 
        else:
            return None 

    def save_name_itent(self,conversacion,name_itent):

        try:
            print("save_name_itent")
            db = self.con
            col = db['conversaciones']

            lista_itents= self.get_trace_itents(conversacion)
            name_itent = f'{name_itent}'
            lista_itents.append(name_itent)

            query = {"_id":ObjectId(conversacion)}
            new_state = { "$set": {"name_itent":lista_itents} }   
            col.update_many(query,new_state)
       
        except:
            print(sys.exc_info())
    def check_conversaciones_inactivos(self):
        print("check_conversaciones_inactivos")
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"estadoBot":"ATENDIENDO"}

        docs = col.find(query,{"_id":1,"lastMessageDateBot":1,"origen":1,"name_itent":1})

        if db.conversaciones.count_documents(query) != 0:
            #return docs
            self.var_check_conversaciones_inactivos= docs
        else:
            self.var_check_conversaciones_inactivos = None

    def check_conversaciones_radar(self):
        print("check_conversaciones_radar")
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"estadoBot":"RADAR"}

        result = col.find(query,{"_id":1,"origen":1})

        lista_result = list(result)
        
        # print(lista_result[0]["origen"])
        
        if db.conversaciones.count_documents(query) != 0:
            return lista_result
        else:
            return None    


    def check_conversaciones_espera(self):
        print("check_conversaciones_espera")
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"estadoBot":{"$in": ["ESCALADO","JALADO_X_AGENTE"]},"estado":"NO_ATENDIDO"}

        docs = col.find(query,{"_id":1,"origen":1,"name_profile":1,"lastMessageDateBot":1})
        lista_docs = list(docs)

        if db.conversaciones.count_documents(query) != 0:

            return lista_docs
           
        else:
            return None

    def check_conversaciones_espera_en_curso(self):
        print("check_conversaciones_espera_en_curso")
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"estadoBot":{"$in": ["ESCALADO","JALADO_X_AGENTE"]},"estado":"ATENDIENDO"}

        docs = col.find(query,{"_id":1,"origen":1,"name_profile":1,"nuevosMensajes":1,"fechaAtendido":1,"agente":1})
        lista_docs = list(docs)

        if db.conversaciones.count_documents(query) != 0:
            return lista_docs         
        else:
            return None              

    def get_fecha_ultimo_mensaje_agente(self,conversacion):
        print("get_ultimo_mensaje_agente")
        self.conect()
        db = self.con
      
        # Buscar el último mensaje del agente en la conversación específica
        query = {
            "rol": "agente",
            "conversacion": ObjectId(conversacion)  # Pasar el ID de la conversación como cadena
        }
        projection = {"createdAt": 1}  # Obtener solo el campo de fecha
        mensajes_col = db['mensajes']
        ultimo_mensaje = mensajes_col.find(query, projection).sort("createdAt", -1).limit(1)

        # Comprobar si se encontró algún mensaje
        if mensajes_col.count_documents(query) > 0:
            return ultimo_mensaje[0]["createdAt"]
        else:
            return None  # No se encontraron mensajes del agente en esta conversación
    
    def get_fecha_ultimo_mensaje_cliente(self,conversacion):
        print("get_fecha_ultimo_mensaje_cliente")
        self.conect()
        db = self.con
      
        # Buscar el último mensaje del agente en la conversación específica
        query = {
            "rol": "cliente",
            "conversacion": ObjectId(conversacion)  # Pasar el ID de la conversación como cadena
        }
        projection = {"fecha": 1}  # Obtener solo el campo de fecha
        mensajes_col = db['mensajes']
        ultimo_mensaje = mensajes_col.find(query, projection).sort("fecha", -1).limit(1)

        # Comprobar si se encontró algún mensaje
        if mensajes_col.count_documents(query) > 0:
            return ultimo_mensaje[0]["fecha"]
        else:
            return None  # No se encontraron mensajes del agente en esta conversación
        
    def close_conversaciones_inactivos(self,id):
        print("close_conversaciones_inactivos")
        print(id)
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"_id":ObjectId(id)}
        new_state = { "$set": { "estado":"ATENDIDO","estadoBot":"ATENDIDO","fechaTerminado":datetime.datetime.now(), "idx_estado.nombre":"ATENDIDO","idx_estado.clave":2} }

        col.update_many(query,new_state)

    def escalar_conversaciones_inactivos(self,id):
        print("escalar_conversaciones_inactivos")
        print(id)
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"_id":ObjectId(id)}
        new_state = { "$set": { "estado":"NO_ATENDIDO","estadoBot":"ESCALADO", "idx_estado.nombre":"NO_ATENDIDO","idx_estado.clave":0} }
        new_state2 = {"$unset": { "agente": "" }}

        col.update_many(query,new_state)
        col.update_many(query,new_state2)

    def get_trace_agentes(self,conversacion):
        try:
            print("### agentes ###")
            db = self.con
            col = db['conversaciones']

            query = {"_id":ObjectId(conversacion)}
      
            result = col.find_one(query,{"iteracion_agentes":1})

            var_name_itent = result.get('iteracion_agentes', ["0"])

            return var_name_itent
       
        except:
            print(sys.exc_info())

    def get_name_agent(self,id):
        try:
            print("### get_name_agent ###")
            db = self.con
            col = db['agentes']

            query = {"_id":ObjectId(id)}
      
            result = col.find_one(query,{"nombre":1})

            var_name_itent = result.get('nombre', ["0"])

            return var_name_itent
       
        except:
            print(sys.exc_info())

    def save_name_agentes(self,conversacion,name_itent):

        try:
            print("save_name_agentes")
            db = self.con
            col = db['conversaciones']

            lista_itents= self.get_trace_agentes(conversacion)
            # name_itent = f'{len(lista_itents)}.{name_itent}'
            lista_itents.append(ObjectId(name_itent))

            query = {"_id":ObjectId(conversacion)}
            new_state = { "$set": {"iteracion_agentes":lista_itents} }   
            col.update_many(query,new_state)
       
        except:
            print(sys.exc_info())

    def liberar_conversaciones_sin_gestion(self,id,agente):
        print("liberar_conversaciones_sin_gestion")
        print(id)
        self.conect()
        db = self.con
        col = db['conversaciones']

        

        query={"_id":ObjectId(id)}
        new_state = { "$set": { "estado":"NO_ATENDIDO","estadoBot":"ESCALADO", "idx_estado.nombre":"NO_ATENDIDO","idx_estado.clave":0,"moveKey":"Liberado,Sin Gestión +3m"} }
        new_state2 = {"$unset": { "agente": "" }}

        col.update_many(query,new_state)
        col.update_many(query,new_state2)

        name_agente = self.get_name_agent(agente)
        self.save_name_agentes(id,name_agente)


    def insert_chatBot(self,mensaje,id,hora,id_msg,type_messege,channelId,platform,caption,estadoEnvio):
        print("insert_chat Bot"+str(type_messege)+":"+str(mensaje))
        self.conect()
        db = self.con

        fecha_dt = datetime.datetime.now()

        col = db['mensajes']
        try:


            query={"rol":"bot","persona":"Wappito","texto":mensaje,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId,"estadoEnvio":estadoEnvio}
            col.insert_one(query)

        except:
            print("Unexpected error:", sys.exc_info()[0])
