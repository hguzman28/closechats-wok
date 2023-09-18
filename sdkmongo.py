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


    def conect(self):
        #DB = "iContactdb"
        #URL_DB = ""
        client = pymongo.MongoClient("mongodb://hguzman:Abcd.1234@cluster0-shard-00-00-ot7rd.mongodb.net:27017,cluster0-shard-00-01-ot7rd.mongodb.net:27017,cluster0-shard-00-02-ot7rd.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        db = client["WOK"]
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

        docs = col.find(query,{"_id":1,"lastMessageDateBot":1,"origen":1})

        if db.conversaciones.count_documents(query) != 0:
            #return docs
            self.var_check_conversaciones_inactivos= docs
        else:
            self.var_check_conversaciones_inactivos = None


    def close_conversaciones_inactivos(self,id):
        print("close_conversaciones_inactivos")
        print(id)
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"_id":ObjectId(id)}
        new_state = { "$set": { "estado":"ATENDIDO","estadoBot":"ATENDIDO","fechaTerminado":datetime.datetime.now()} }

        col.update_many(query,new_state)

    def insert_chatBot(self,mensaje,id,hora,id_msg,type_messege,channelId,platform,caption,estadoEnvio):
        print("insert_chat Bot"+str(type_messege)+":"+str(mensaje))
        self.conect()
        db = self.con

        fecha_dt = datetime.datetime.now()

        col = db['mensajes']
        try:


            query={"rol":"agente","texto":mensaje,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId,"estadoEnvio":estadoEnvio}
            col.insert_one(query)

        except:
            print("Unexpected error:", sys.exc_info()[0])
