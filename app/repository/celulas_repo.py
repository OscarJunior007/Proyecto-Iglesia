from pydantic import BaseModel, Field
from fastapi import HTTPException
from uuid import uuid4
import mysql.connector


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
def ActualiozarBD():
    connection = mysql.connector.connect(user='root', password='12345',
                                         database='bd_iglesia',
                                         port='3306')
    return connection


def create_celula(datos: Celula):
    conexion = ActualiozarBD()
    cursor = conexion.cursor()

    query = """
        INSERT INTO celulas (id,lider_cedula,dia_celula,direccion,nombre_celula,name_lider,name_anfitrion,name_sublider)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        datos.id,  # Asegúrate de incluir la cédula del líder
        datos.lider_cedula,
        datos.dia_celula,
        datos.direccion,        
        datos.nombre_celula,
        datos.name_lider,
        datos.name_anfitrion, 
        datos.name_sublider,
    )

    cursor.execute(query, values)
    conexion.commit()
    cursor.close()

def extract_celula(cedula):
    conexion = ActualiozarBD()
    cursor = conexion.cursor(dictionary=True)

    try:
        query = "SELECT * FROM celulas WHERE lider_cedula = %s"
        cursor.execute(query, (cedula,))
        reparaciones = cursor.fetchall()  

        return reparaciones  
    except TypeError as e:
        raise HTTPException(status_code=500, detail=f"ERROR AL OBTENER LOS DATOS: {e}")
    finally:
        cursor.close()
        conexion.close()


