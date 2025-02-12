import mysql.connector
from fastapi import HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

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

    conexion = ActualiozarBD()

    cursor = conexion.cursor(dictionary= True)

    try:
       query = f" SELECT *  FROM Users where cedula_user = '{cedula}' "
       cursor.execute(query)
       reparaciones = cursor.fetchone() # AGARRO TODAS LAS FILAS DE LA TABLA.

       return User(**reparaciones)

    except TypeError as e:
     raise HTTPException(status_code= 500, detail= f"ERROR AL OBTENER LOS DATOS: {e}")
    finally:
       cursor.close()
       conexion.close()

def create_user(datos: User):
   
     conexion = ActualiozarBD()

     cursor = conexion.cursor()

     query =  """
             INSERT INTO Users (id, nombre,direccion,email, profile,numero_celular,cedula_user)
             VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
     values = (
               datos.id,
               datos.nombre,
               datos.direccion,
               datos.email,
               datos.profile,
               datos.numero_celular,
               datos.cedula_user
                )
    
     cursor.execute(query,values)
     conexion.commit()
     cursor.close()
