from fastapi import FastAPI, HTTPException
from app.repository import celulas_repo,celulas_repo_firestore,reuniones_repo_firestore
from app.schemas import SystemUser 
from app.schemas import Celula, Reunion
from fastapi import FastAPI, status, HTTPException, Depends
from app.deps import get_current_user

def setup3(app:FastAPI):
    @app.post("/register/reuniones/{id_celula}")
    def register_reuniones(reunion: Reunion, user: SystemUser = Depends(get_current_user)):
     try:
        
        reuniones_repo_firestore.create_reunion(reunion)
        
        return {"message": "Célula registrada exitosamente", "celula": reunion.dict()}
     except Exception as e:
        print(f"Error al registrar célula: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno en el servidor: {e}")
     

    @app.get("/api/reuniones/registradas")
    def get_celulas(id_celula: str):
        
      try:
         datos = reuniones_repo_firestore.extract_reunion(id_celula)
      except Exception as e:
         raise HTTPException(status_code=404, detail="No se encontraron datos para esta reunion") 
            
      if not datos:
         return[]
      return datos