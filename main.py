
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

url = "https://graph.facebook.com/v15.0/144272775427424/messages"
TOKEN_WA = "EAAD4RcNvz3IBO4Q1xaZCpnESRXu3fFVlS5w4ZAh2htUvjaDZBOuZCSxazBimJOTsqh2mII8RGY5IycnSsUUL6JVdZCXduZCBgCvK5NzTrpvZAaoEKgh7cEYvrHjZCtN4DRyBjZC62q9W1ZAHDGEMIozUzq6eUj8aJXz0II1hcIL4xeqTgTGLGNzqRV7GAWU1EPtv54HZB7e"

def send_menu_interactive_button(num_client,id_conversacion,TOKEN_WA,url):
    
    try:
      
        mensaje = "Estimado cliente, no hemos recibido respuesta, cerramos esta conversación y estamos atento para volver a atenderte. \n\n ℹ️ Sí ya tenías un pedido en este chat, favor volver a escribir, tomar opción como va mi pedido"

        body={
              "type": "button",
              "header": {
                "type": "text",
                "text": "ℹ️"
              },
              "body": {
                "text": mensaje
              },
              "footer": {
                "text": "Restaurante Wok Q'rrambero 🍜"
              },
              "action": {
                    "buttons": [
                    {
                      "type": "reply",
                      "reply": {
                        "id": "returnClien",
                        "title": "Cotizar o Pedir" 
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
        db.insert_chatBot(mensaje,id_conversacion,datetime.datetime.now(),None,"text","","whatsapp",None,"true")

        print(response)
    except:
        print("except")
        print(str(sys.exc_info())) 

def send_menu_interactive(num_client,id_conversacion,mensaje,TOKEN_WA,url):
    
    try:
        print("send_menu_interactive")
        
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": ""+num_client+"",
        "text": {
            "body": ""+mensaje+""
        }
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
        db.insert_chatBot(mensaje,id_conversacion,datetime.datetime.now(),None,"text","","whatsapp",None,"true")

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
            print(df.head(5))
       
            # name_itent = list(df["name_itent"].values)
            # print(type(name_itent))
            # print(name_itent[0])

            # if any("menu_ppal" in intent for intent in name_itent[0]):
            #     print("PILAS, HAY INTERES")



            var_hoy = datetime.datetime.now()
            df['TIEMPO_INACTIVIDAD'] = var_hoy  - df['lastMessageDateBot']
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=13), "CERRAR" ] = True
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=3), "RECALENTAMIENTO" ] = True
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=5), "ESCALAR" ] = True
            df['INTERES'] = df['name_itent'].apply(lambda x: any("menu_ppal" in intent for intent in x))

            print(df)


            for index, row in df.iterrows():
                

                if row['CERRAR'] is True and row["INTERES"] is False:
                    print(index, row)
                    db.close_conversaciones_inactivos(row['_id'])
                    db.save_name_itent(row['_id'],"CLIENTE_SIN_RESPUESTA")
                    print(row['origen'])
                    send_menu_interactive_button(row['origen'],row['_id'],TOKEN_WA,url)
                elif row['RECALENTAMIENTO'] is True and row["INTERES"] is True:
                    db.save_name_itent(row['_id'],"RECALENTAMIENTO_CLIENTE")
                    send_menu_interactive(row['origen'],row['_id'],"Estimado cliente, favor usar algunas de las opciones suministrada👆",TOKEN_WA,url)
                elif row['ESCALAR'] is True and row["INTERES"] is True:
                    db.save_name_itent(row['_id'],"CLIENTE_CON_INTERES_SIN_RESPUESTA")
                    send_menu_interactive(row['origen'],row['_id'],"Estimado cliente, a continuación uno de nuestros asesores lo atenderá",TOKEN_WA,url)
                    db.escalar_conversaciones_inactivos(row['_id']) 
                    


    except:
        return {"registro":"Fallido","conversacion":""+str(sys.exc_info())}


lambda_handler(None, None)