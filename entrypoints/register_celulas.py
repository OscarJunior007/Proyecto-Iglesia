from fastapi import FastAPI, HTTPException
from app.repository import celulas_repo,celulas_repo_firestore
from app.schemas import SystemUser 
from app.schemas import Celula

from fastapi import FastAPI, status, HTTPException, Depends
from app.deps import get_current_user
def setup2(app:FastAPI):
    
    @app.post("/register/celulas")
    def register_celulas(celula: Celula, user: SystemUser = Depends(get_current_user)):
     try:
        
        celulas_repo_firestore.create_celula(celula)
        
        return {"message": "Célula registrada exitosamente", "celula": celula.dict()}
     except Exception as e:
        print(f"Error al registrar célula: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno en el servidor: {e}")
     

    @app.get("/celulas/registradas")
    def get_celulas(user: SystemUser = Depends(get_current_user)):
      
      try:
         datos = celulas_repo_firestore.extract_celula(user.cedula_user)
      except Exception as e:
         raise HTTPException(status_code=404, detail="No se encontraron datos para esta cédula") 
 
      if not datos:
          raise HTTPException(status_code=404, detail="No se encontraron datos para esta cédula") 
      return datos
       
          
      
      
   



