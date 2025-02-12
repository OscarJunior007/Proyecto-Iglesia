from uuid import UUID
from pydantic import BaseModel, Field
from uuid import uuid4


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    profile: str = 'DEFAULT' 
class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    celular: str = Field(...,  description="user celular")
    user_direccion: str = Field(..., description="user direccion")
    user_cedula: str = Field(..., description="user cedula")  # Agregar anotación de tipo
    user_nombre: str = Field(..., description="user nombre")  # Agregar anotación de tipo

class UserOut(BaseModel):
    id: UUID
    email: str
    profile:str




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

class SystemUser(UserOut):
    cedula_user: str | None = "123"
    profile: str | None = "DEFAULT"