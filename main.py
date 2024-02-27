
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

# url = "https://graph.facebook.com/v15.0/144272775427424/messages"
# TOKEN_WA = "EAAD4RcNvz3IBO4Q1xaZCpnESRXu3fFVlS5w4ZAh2htUvjaDZBOuZCSxazBimJOTsqh2mII8RGY5IycnSsUUL6JVdZCXduZCBgCvK5NzTrpvZAaoEKgh7cEYvrHjZCtN4DRyBjZC62q9W1ZAHDGEMIozUzq6eUj8aJXz0II1hcIL4xeqTgTGLGNzqRV7GAWU1EPtv54HZB7e"
def send_menu_interactive_button_dinamico(num_client,mensaje,id_conversacion,TOKEN_WA,url):
    
    try:
      
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
                        "title": "Descubrir" 
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
        'Authorization': ''+str(TOKEN_WA)+'',
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
        'Authorization': ''+str(TOKEN_WA)+'',
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
        'Authorization': ''+str(TOKEN_WA)+'',
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


def send_menu_interactive_sin_registro(num_client,id_conversacion,mensaje,TOKEN_WA,url):
    
    try:
        print("send_menu_interactive_sin_registro")
        
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": ""+num_client+"",
        "text": {
            "body": ""+mensaje+""
        }
        })
        

        headers = {
        'Authorization': ''+str(TOKEN_WA)+'',
        'Content-Type': 'application/json'
        }

        print("###########")
        print(payload)
        print("###########")
        print(headers)

        
        response = requests.request("POST", url, headers=headers, data=payload)
        #db.insert_chatBot(mensaje,id_conversacion,datetime.datetime.now(),None,"text","","whatsapp",None,"true")

        print(response)
    except:
        print("except")
        print(str(sys.exc_info())) 
        
       
def lambda_handler(event, context):


    # try:
        db.check_conversaciones_inactivos()
        chats_espera = db.check_conversaciones_espera()
        supervisores = db.check_conversaciones_radar()
        chats_espera_en_curso = db.check_conversaciones_espera_en_curso()
        chats_fuera_dehorario_8h = db.get_conversaciones_fuera_de_horario_ultimas8h()

        # url,TOKEN_WA,token_wompi,token_catalogo,url_catalogo  = db.get_config(os.environ.get("NUM_API1"))
        url,TOKEN_WA,token_wompi,token_catalogo,url_catalogo  = db.get_config("573045847949")

  

        ### Chats que el Bot está atendiendo ######
        if db.var_check_conversaciones_inactivos is not None:

            df = pd.DataFrame(list(db.var_check_conversaciones_inactivos))
            
            var_hoy = datetime.datetime.now()
            df['TIEMPO_INACTIVIDAD'] = var_hoy  - df['lastMessageDateBot']
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=15), "CERRAR" ] = True
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=2), "RECALENTAMIENTO" ] = True
            df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=5), "ESCALAR" ] = True
            # Verificar y reemplazar NaN con una lista vacía en la columna 'name_itent'
            # Verificar y reemplazar NaN con una lista vacía en la columna 'name_itent'
            #df['name_itent'] = df['name_itent'].apply(lambda x: [] if pd.isnull(x) else x)
            
            # Aplicar la función lambda para marcar el interés en 'menu_ppal' usando any()
            #df['INTERES'] = df['name_itent'].apply(lambda x: any("menu_ppal" in intent for intent in x) if isinstance(x, list) else False)

            df['INTERES'] = df['name_itent'].apply(lambda x: any("menu_ppal" in intent for intent in x))
            
            for index, row in df.iterrows():
                

                if row['CERRAR'] is True and row["INTERES"] is False:  ## 15 mins de espera sin inicio cotización
                    print(index, row)
                    db.close_conversaciones_inactivos(row['_id'])
                    db.save_name_itent(row['_id'],"CLIENTE_SIN_RESPUESTA")
                    print(row['origen'])
                    send_menu_interactive_button(row['origen'],row['_id'],TOKEN_WA,url)
                elif row['ESCALAR'] is True and row["INTERES"] is True: ## 5 mins de espera con por lo menos ya inicio ver los productos, cotización o en datos personales
                    db.save_name_itent(row['_id'],"CLIENTE_CON_INTERES_SIN_RESPUESTA")
                    send_menu_interactive(row['origen'],row['_id'],"Estimado cliente, a continuación uno de nuestros asesores lo atenderá",TOKEN_WA,url)
                    db.escalar_conversaciones_inactivos(row['_id'])     
                elif row['RECALENTAMIENTO'] is True: ### Recordar al cliente que estamos atentos despues de 2 mins de espera
                    db.save_name_itent(row['_id'],"RECALENTAMIENTO_CLIENTE")
                    send_menu_interactive(row['origen'],row['_id'],"Estimado cliente, favor usar algunas de las opciones suministrada👆",TOKEN_WA,url)
                
        ### Chats que el Bot escaló y están de espera en atención ######
        if chats_espera is not None:
            try:
              print("DENTRO CHATS EN ESPERA")
              df = pd.DataFrame(chats_espera)
             
              # identificar registros con más chats igual o mayor a 3m
              var_hoy = datetime.datetime.now()

              ##### Mayor a 3 min ######
              df['TIEMPO_INACTIVIDAD'] = var_hoy  - df['lastMessageDateBot']
              df.loc[df['TIEMPO_INACTIVIDAD'] >  datetime.timedelta(minutes=3), "3m" ] = True

              # Filtra las filas donde la columna '3m' es True
              true_values = df[df['3m'] == True]
              print(true_values)
              # Cuenta cuántos valores True hay
              count_true = len(true_values)

              # Suponiendo que true_values['TIEMPO_INACTIVIDAD'] contiene objetos Timedelta
              # Primero, convertimos los timedelta a minutos
              tiempos_en_minutos = true_values['TIEMPO_INACTIVIDAD'] / pd.Timedelta(minutes=1)

              # Luego, los convertimos a cadenas de texto
              tiempos_en_minutos_str = tiempos_en_minutos.astype(str) + ' minutos'

              # Finalmente, unimos todas las partes
              names_with_origen = ', '.join(true_values['name_profile'] + ' (' + true_values['origen'] + ')' + ' - Tiempo espera: ' + tiempos_en_minutos_str)


              # Crea una cadena con los nombres separados por coma
            #   names = ', '.join(true_values['name_profile'])
            #   names_with_origen = ', '.join(true_values['name_profile'] + ' (' + true_values['origen'] + ')'+'-Tiempo espera: '+true_values['TIEMPO_INACTIVIDAD'])
              print(names_with_origen)

          
              # Agrega la primera línea del mensaje con la cantidad de clientes}
              mensaje_lines = []
              mensaje_lines.append(f"📊 WappiRadar informa, que tiene(s) {count_true} cliente(s) con o más de 3 min de espera:")

              # Recorre los clientes y agrega una línea para cada uno
              for index, row in true_values.iterrows():
                  nombre_perfil = row['name_profile']
                  numero_telefono = row['origen'] 
                  tiempo_espera_minutos = row['TIEMPO_INACTIVIDAD'].total_seconds() / 60
                  mensaje_lines.append(f"{nombre_perfil} ({numero_telefono}) - Tiempo espera: {tiempo_espera_minutos:.2f} minutos")

              # Une todas las líneas del mensaje en una sola cadena
              mensaje = "\n".join(mensaje_lines)

              for index, row in df.iterrows():
                  
                  if row['3m'] is True:
                      print(index, row)
                      #db.save_name_itent(row['_id'],"CLIENTE_ENESPERA_3M")
                      for super in supervisores:
                        print(super["origen"])
                        # send_menu_interactive_sin_registro(super["origen"],row['_id'],f"📊 WappiRadar informa, que tiene(s) *{count_true}* cliente(s) con o más de 3 min de espera, \n\n sus nombre de perfile son:\n _{names_with_origen}_",TOKEN_WA,url)
                        send_menu_interactive_sin_registro(super["origen"],row['_id'],mensaje,TOKEN_WA,url)

              #for index,row in true_values.iterrows():
              #    send_menu_interactive(row['origen'],row['_id'],"Gracias por la espera. Un asesor lo atenderá en breve",TOKEN_WA,url)
            except:
                print(sys.exc_info())   

        ### Chats q están en atención por un agente ######         
        if chats_espera_en_curso is not None:
            try:
                print("DENTRO CHATS EN chats_espera_en_curso")
                df = pd.DataFrame(chats_espera_en_curso)
                
                # identificar registros con chats igual o mayor a 3m
                var_hoy = datetime.datetime.now()
                df['TIEMPO_ATENCION'] = var_hoy  - df['fechaAtendido']
                df.loc[df['TIEMPO_ATENCION'] >  datetime.timedelta(minutes=3), "ta3m" ] = True

                # Filtra las filas donde la columna 'ta3m' es True
                df_ta3m = df[df['ta3m'] == True]

                for index, row in df_ta3m.iterrows():
                  if row['ta3m'] is True:
                      
                      # Fechas de ultimo mensaje de cliente y agente
                      fecha_ultimo_mensaje_agente = db.get_fecha_ultimo_mensaje_agente(row['_id'])
                      fecha_ultimo_mensaje_cliente = db.get_fecha_ultimo_mensaje_cliente(row['_id'])
                      
                      #### Definimos quien espera a quien ################
                      quien_espera = 0 # Por defecto, Espera cliente a WOK   
                      #if fecha_ultimo_mensaje_agente is not None:
                      if fecha_ultimo_mensaje_agente is not None and fecha_ultimo_mensaje_cliente is not None:  
                        if fecha_ultimo_mensaje_agente > fecha_ultimo_mensaje_cliente:
                            quien_espera = 1 # Espera wok a cliente
                        else:
                            quien_espera = 0 # Espera cliente a WOK   
                      
                      ### Según quien espera, tomamos deciciones #########
                      if  quien_espera == 0: # Espera cliente a WOK  
                        if fecha_ultimo_mensaje_agente is None: ## Caso donde chat dieron click en atender, pero no ha sido gestionado por agente
                            db.liberar_conversaciones_sin_gestion(row['_id'],row['agente'])
                        elif var_hoy - fecha_ultimo_mensaje_agente >= datetime.timedelta(minutes=3): ## If tiempo sin gestion es mayor a 3 mins
                            db.liberar_conversaciones_sin_gestion(row['_id'],row['agente'])
                      else: # Espera wok a cliente
                        if var_hoy - fecha_ultimo_mensaje_cliente >= datetime.timedelta(minutes=10): ## If tiempo sin gestion es mayor a 10 mins
                            db.liberar_conversaciones_sin_gestion(row['_id'],row['agente'])

                            
                      #db.save_name_itent(row['_id'],"CLIENTE_ENESPERA_3M")
                    #   for super in supervisores:
                    #     print(super["origen"])
                    #     send_menu_interactive_sin_registro(super["origen"],row['_id'],f"📊 WappiRadar informa, que tiene(s) *{count_true}* cliente(s) con o más de 3 min de espera, \n\n sus nombre de perfile son:\n _{names_with_origen}_",TOKEN_WA,url)

            except:
               print(sys.exc_info())     

        if chats_fuera_dehorario_8h is not None:
            try:
                print("DENTRO chats_fuera_dehorario_8h")
                df = pd.DataFrame(chats_fuera_dehorario_8h)

                for index, row in df.iterrows():
                    send_menu_interactive_button_dinamico(row['origen'],"Estimado cliente, nos encontramo en horario hábil, haz tú pedido",row['_id'],TOKEN_WA,url)
                    db.cliente_notificacido_disponibilidad_horario(row['_id'])



            except:
               print(sys.exc_info()) 

    # except:
    #     return {"registro":"Fallido","conversacion":""+str(sys.exc_info())}


lambda_handler(None, None)
