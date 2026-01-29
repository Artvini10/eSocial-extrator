from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routes.onboarding import router
from src.services.orchestrator import expandir_temas
from src.services.ws_adapter import WSEsocialAdapter

app = FastAPI(title="Extrator eSocial")

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(router)

@app.post("/executar_ws")
async def executar_ws(cnpj: str, ambiente: str, temas: list[str], periodo: str):
    eventos = expandir_temas(temas)
    ws = WSEsocialAdapter(cnpj, ambiente)
    retorno = ws.executar(eventos, periodo)
    return {"eventos_executados": eventos, "retorno": retorno}