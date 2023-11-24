from pymongo import MongoClient
from bson import ObjectId
import datetime

def obtener_ultimo_mensaje_agente():
    client = MongoClient('mongodb://hguzman:Abcd.1234@cluster0-shard-00-00-ot7rd.mongodb.net:27017,cluster0-shard-00-01-ot7rd.mongodb.net:27017,cluster0-shard-00-02-ot7rd.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['WOK']
    
    conversacion_id = "654a6bd5407ab88d5e617253"  # El ID de la conversación en cuestión
    
    # Buscar el último mensaje del agente en la conversación específica
    query = {
        "rol": "agente",
        "conversacion": ObjectId(conversacion_id)  # Pasar el ID de la conversación como cadena
    }
    projection = {"createdAt": 1}  # Obtener solo el campo de fecha
    
    mensajes_col = db['mensajes']
    ultimo_mensaje = mensajes_col.find(query, projection).sort("createdAt", -1).limit(1)
   
    
    # Comprobar si se encontró algún mensaje
    if mensajes_col.count_documents(query) > 0:
        return ultimo_mensaje[0]["createdAt"]
    else:
        return None  # No se encontraron mensajes del agente en esta conversación

# Llamada a la función para obtener la fecha del último mensaje del agente en la conversación
fecha_ultimo_mensaje = obtener_ultimo_mensaje_agente()
print("Fecha del último mensaje del agente:", fecha_ultimo_mensaje)
TSG = datetime.datetime.now() - fecha_ultimo_mensaje
print(type(TSG))
print(TSG)

if TSG > datetime.timedelta(minutes=3):
    print("mayor")
else:
    print("menor")    

