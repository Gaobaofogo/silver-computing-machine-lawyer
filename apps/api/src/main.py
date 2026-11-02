from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Judis-Advocacia API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from apps.api.src.schemas.cliente import ClienteSchema

@app.post("/clientes")
def criar_cliente(cliente: ClienteSchema):
    return{"status":"criado","cliente":cliente.model_dump()}

@app.get("/health")
def health():
    return {"status": "ok", "project": "judis-advocacia"}
