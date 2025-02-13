from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from entrypoints import security,register_celulas,register_reuniones,reports

app = FastAPI()

templateJinja = Jinja2Templates(directory="templates", )


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security.setup(app)
reports.setup(app)
register_celulas.setup2(app)
register_reuniones.setup3(app)

@app.get("/register", response_class=HTMLResponse)
def root(request: Request):
    return templateJinja.TemplateResponse("register.html", {
        "request": request,
        "base_url": str(request.base_url)  # URL base para usar en Jinja
    })

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templateJinja.TemplateResponse("login.html", {
        "request": request,
        "base_url": str(request.base_url)
    })

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templateJinja.TemplateResponse("home.html", {
        "request": request,
        "base_url": str(request.base_url)
    })

@app.get("/create_celula", response_class=HTMLResponse)
def create_celula(request: Request):
    return templateJinja.TemplateResponse("create_celula.html", {
        "request": request,
        "base_url": str(request.base_url)
    })

@app.get("/celulas", response_class=HTMLResponse)
def celulas(request: Request):
    return templateJinja.TemplateResponse("celulas.html", {
        "request": request,
        "base_url": str(request.base_url)
    })

@app.get("/reuniones/{id_celula}", response_class=HTMLResponse)
def reuniones(request: Request, id_celula: str):
    return templateJinja.TemplateResponse("reuniones.html", {
        "request": request,
        "base_url": str(request.base_url),
        "id_celula": id_celula
    })

@app.get("/report", response_class=HTMLResponse)
def report(request: Request):
    return templateJinja.TemplateResponse("report.html", {
        "request": request,
        "base_url": str(request.base_url)
    })


import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)