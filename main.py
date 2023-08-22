
import datetime
import sys
import json
import pymongo
import re
import datetime
import sys
from bson import ObjectId
import sdkmongo
import os
import pandas as pd
import requests
import numpy

db = sdkmongo.DB()

def sent_message_client(tel,mensaje,id_conversacion,channelId):
    url = "https://conversations.messagebird.com/v1/send"
    # Definimos la cabecera y el diccionario con los datos
    cabecera1 = {'Content-type': 'application/json', 'Authorization':'AccessKey 9aw3ghvwgXHsT2gUzsTXKX13u'}
    datos = '{ "to":"'+tel+'", "from":"5633a3c8ed6a4850929bc4c1a0636249", "type":"text", "content":{ "text":"'+mensaje+'" }, "reportUrl":"https://example.com/reports" }'

    solicitud = requests.post(url, headers = cabecera1, data = datos)

    db.insert_chatBot(mensaje,id_conversacion,datetime.datetime.now(),None,"text",channelId,"whatsapp",None,"true")
    print(solicitud.text)

def send_menu_interactive_button(num_client):
    
    try:
        url = "https://graph.facebook.com/v15.0/110194322139284/messages"
        TOKEN_WA = "EAAD4RcNvz3IBO13q6ONhNRTa558lV2nD33deAvu6zm9aJIaw9hKLyfuWXtPO7Dmx2RoGyzRkub1WZAhmbzjj6DYwRpf8tpOTNwupaSyPA0TPhHHYWIYvJ2U1gczvhS5p97oAOVTIBCak5nAZAGNWQLZAJhyLpq9CIO1RT8ViHtNMiDipvZAfTEImvk1YMKgYLtRH"


        body={
            "type": "button",
            "header": {
                "type": "text",
                "text": "ℹ️"
            },
            "body": {
                "text": "Estimado cliente, no hemos recibido respuesta, cerramos esta conversación y estamos atento para volver a atenderte"
            },
            "footer": {
                "text": "Restaurante Wok Q'rrambero 🍜"
            },
            "action": {
                    "buttons": [
                    {
                    "type": "reply",
                    "reply": {
                        "id": "returnCli",
                        "title": "Quiero pedir de nuevo" 
                    }
                    }
                ] 
            }
            }
        
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": ""+str(num_client)+"",
        "type": "interactive",
        "interactive": body

        })

        headers = {
        'Authorization': 'Bearer '+str(TOKEN_WA)+'',
        'Content-Type': 'application/json'
        }

        print("###########")
        print(payload)
        print("###########")
        print(headers)

        
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response)
    except:
        print("except")
        print(str(sys.exc_info())) 



def lambda_handler(event, context):


    try:
        db.check_conversaciones_inactivos()

        if db.var_check_conversaciones_inactivos is not None:

        #result = check_conversaciones_inactivos()

            df = pd.DataFrame(list(db.var_check_conversaciones_inactivos))
            var_hoy = datetime.datetime.now()
            df['TIEMPO_INACTIVIDAD'] = var_hoy  - df['lastMessageDateBot']
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=13), "CERRAR" ] = True


            for index, row in df.iterrows():

                if row['CERRAR'] is True:
                    print(index, row)
                    mensaje = "Estimado cliente, no obtuvimos respuesta en un tiempo determinado, procedemos a cerrar la conversacion, para consultas puede volver a escribirnos."
                    db.close_conversaciones_inactivos(row['_id'])
                    print(row['origen'])
                    send_menu_interactive_button(row['origen'])
                else:
                    print("no hay nada q cerrar")


    except:
        return {"registro":"Fallido","conversacion":""+str(sys.exc_info())}
