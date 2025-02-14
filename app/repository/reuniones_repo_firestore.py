from pydantic import BaseModel, Field
from fastapi import HTTPException
from uuid import uuid4
import mysql.connector
from  functools import cache
import collections
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

class Reunion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Convierte UUID a str
    fecha_reunion : str
    asistencias_celula : str
    new_people : str
    asisten_iglesia : str
    celulaId: str

  

# Función para conectar a la base de datos
# def ActualiozarBD():
#     connection = mysql.connector.connect(user='root', password='12345',
#                                          database='bd_iglesia',
#                                          port='3306')
#     return connection



def create_reunion(datos: Reunion):
    # Inicializa el cliente
    db = firestore.Client()

    # Agregar datos con un ID automático
    db.collection('reuniones').document(f"{datos.celulaId}-{datos.fecha_reunion}").set(datos.dict())

    print("Célula creada correctamente.")

    

def extract_reunion(id):
    db = firestore.Client()

    try:
        usuarios_ref = db.collection('reuniones')
        query = usuarios_ref.where('celulaId', '==', id)
        docs = query.stream()

        reuniones = [doc.to_dict() for doc in docs] 
        return reuniones if reuniones else []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ERROR AL OBTENER LOS DATOS: {e}")




def get_report():
   db = firestore.Client()

   try:
        reuniones_ref = db.collection('reuniones')
        docs_reuniones = reuniones_ref.stream()
        result = []
        for doc in docs_reuniones:
            d=doc.to_dict()
            print(d)
            celula = _get_celula(d['celulaId'])
            lider = _get_lider(celula['lider_cedula'])
            result.append( collections.OrderedDict(list(lider.items()))      | collections.OrderedDict(list(celula.items()))    | collections.OrderedDict(list(d.items()))     )

        return result
   except Exception as e:
    print(e)
    return []
   
@cache
def _get_celula(id):
        db = firestore.Client()
        usuarios_ref = db.collection('celulas').document(id)
        return usuarios_ref.get().to_dict()


@cache
def _get_lider(id):
        db = firestore.Client()
        usuarios_ref = db.collection('users').document(id)
        return usuarios_ref.get().to_dict()
