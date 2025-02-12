from pydantic import BaseModel, Field
from fastapi import HTTPException
from uuid import uuid4
import mysql.connector


import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './calendar-449323-536c5b560c7e.json'
from google.cloud import  firestore


class Celula(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Convierte UUID a str
    lider_cedula: str
    dia_celula: str
    direccion: str
    nombre_celula: str
    name_lider: str
    name_anfitrion: str
    name_sublider: str

  

# Función para conectar a la base de datos
# def ActualiozarBD():
#     connection = mysql.connector.connect(user='root', password='12345',
#                                          database='bd_iglesia',
#                                          port='3306')
#     return connection



def create_celula(datos: Celula):
    # Inicializa el cliente
    db = firestore.Client()

    # Agregar datos con un ID automático
    db.collection('celulas').document(datos.id).set(datos.dict())

    print("Célula creada correctamente.")

    

def extract_celula(celula):
   db = firestore.Client()

   try:
        usuarios_ref = db.collection('celulas')
        query = usuarios_ref.where('lider_cedula', '==', f'{celula}')
        docs = query.stream()


        return [doc.to_dict() for doc in docs] if docs else []

   except Exception as e:
     raise HTTPException(status_code= 500, detail= f"ERROR AL OBTENER LOS DATOS: {e}")

