from fastapi import FastAPI, status, HTTPException,Body
from fastapi.responses import RedirectResponse
from app.schemas import UserOut, UserAuth
from app.utils import get_hashed_password
from uuid import uuid4

from app.adapters import correo

from jose import jwt
from app.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from app.schemas import TokenPayload, SystemUser

from app.repository import user_repo, user_repo_firestore
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2
from fastapi.responses import RedirectResponse
from app.schemas import UserOut, UserAuth, TokenSchema, SystemUser
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
   
)
from uuid import uuid4
from app.deps import get_current_user


def setup(app: FastAPI):
     
    @app.post('/signup', summary="Create new user", response_model=UserOut)
    async def create_user(data: UserAuth,user: SystemUser = Depends(get_current_user)):
        
        print(f"esta esla informacion: {data.email}")
        if user.profile != 'ADMIN':
         raise HTTPException(status_code=403, detail=f"Prohibido")
        # querying database to check if user already exist
        user = user_repo_firestore.buscar_user(data.user_cedula)
        if user is not None:    
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist"
            )
        user = {
              'email': data.email,  
                'nombre': data.user_nombre,
                'numero_celular': data.celular,  
                'direccion': data.user_direccion,
                'cedula_user': data.user_cedula, 
                'profile': "default",  
                'id': str(uuid4())
        }

        
        user_repo_firestore.create_user(user_repo.User(**user))     # saving user to database

        correo.EnviarCorreo(data.email,data.user_nombre)

        return user


    @app.post('/api/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
    async def login(cedula: str = Body(..., embed=True)):  # Recibe solo la cédula
        user = user_repo_firestore.buscar_user(cedula)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cédula incorrecta o usuario no encontrado"
            )
          
        return {
            "access_token": create_access_token(user['cedula_user'], user['profile']),
            "refresh_token": create_refresh_token(user['cedula_user'],user['profile'])
        }
    
   

           
    @app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
    async def get_me(user: SystemUser = Depends(get_current_user)):

        print(user)
        return user



        
    @app.get('/emails', summary='Get details of currently logged in user', response_model=UserOut)
    async def get_email(user: SystemUser = Depends(get_current_user)):
        print(user)
        return user.id
