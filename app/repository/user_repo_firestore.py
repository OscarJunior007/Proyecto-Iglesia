import mysql.connector
from fastapi import HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './calendar-449323-536c5b560c7e.json'
from google.cloud import  firestore
class User(BaseModel):
   id : str = Field(default_factory = uuid4)
   nombre: str
   direccion: str
   email: str
   profile : str|None = "ADMIN"
   numero_celular: str
   cedula_user: str


def ActualiozarBD():
    connection = mysql.connector.connect(user='root',password='12345',
                                         database='bd_iglesia',
                                         port='3306'
                                         ) 
    
    return connection

def buscar_user(cedula):

    db = firestore.Client()

    try:
        doc_ref = db.collection('users').document(f'{cedula}')
        doc = doc_ref.get()

        return doc.to_dict() if doc else None

    except Exception as e:
     raise HTTPException(status_code= 500, detail= f"ERROR AL OBTENER LOS DATOS: {e}")

def create_user(datos: User):
   

   
    # Inicializa el cliente
    db = firestore.Client()

    # Agregar datos
    doc_ref = db.collection('users').document(datos.cedula_user)
    doc_ref.set(datos.dict())
    

