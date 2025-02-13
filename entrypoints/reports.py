from fastapi import FastAPI, HTTPException
from app.repository import celulas_repo,celulas_repo_firestore,reuniones_repo_firestore
from app.adapters import excel_adapter
from app.schemas import SystemUser 
from app.schemas import Celula
import uuid
import traceback
from fastapi.responses import StreamingResponse

from fastapi import FastAPI, status, HTTPException, Depends
from app.deps import get_current_user


def setup(app:FastAPI):
    @app.get("/api/report")
    def report(user: SystemUser = Depends(get_current_user)):
     print(user)
     if user.profile != 'ADMIN':
         raise HTTPException(status_code=403, detail=f"Prohibido")
     try:
        
        data =reuniones_repo_firestore.get_report()

        name =  str(uuid.uuid4())
        excel_adapter.export(data,name)
        def iterfile():  # (1)
            with open(name, mode="rb") as file_like:  # (2)
                yield from file_like  # (3)

        return StreamingResponse(iterfile(), media_type="application/vnd.ms-excel")
     except Exception as e:
        print(f"Error al registrar célula: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error interno en el servidor: {e}")