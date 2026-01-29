from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from src.services.orchestrator import expandir_temas
from src.services.ws_adapter import WSEsocialAdapter

router = APIRouter()

# Resolve template path relative to src directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/", response_class=HTMLResponse)
async def acesso(request: Request):
    return templates.TemplateResponse("acesso.html", {"request": request})


@router.post("/acesso")
async def salvar_acesso(
    cnpj: str = Form(...),
    ambiente: str = Form(...),
    cert_tipo: str = Form(...),
    lgpd: str = Form(...),
):
    resp = RedirectResponse(url="/checklist", status_code=303)
    resp.set_cookie("cnpj", cnpj, httponly=True, samesite="strict")
    resp.set_cookie("ambiente", ambiente, httponly=True, samesite="strict")
    resp.set_cookie("cert_tipo", cert_tipo, httponly=True, samesite="strict")
    return resp


@router.get("/checklist", response_class=HTMLResponse)
async def checklist(request: Request):
    cnpj = request.cookies.get("cnpj", "")
    ambiente = request.cookies.get("ambiente", "producao_restrita")
    cert_tipo = request.cookies.get("cert_tipo", "A1")

    return templates.TemplateResponse(
        "checklist.html",
        {"request": request, "cnpj": cnpj, "ambiente": ambiente, "cert_tipo": cert_tipo, "resultado": None},
    )


@router.post("/checklist", response_class=HTMLResponse)
async def executar_checklist(
    request: Request,
    ano_ini: int = Form(...),
    mes_ini: int = Form(...),
    ano_fim: int = Form(...),
    mes_fim: int = Form(...),
    temas: list[str] = Form(default=[]),
):
    cnpj = request.cookies.get("cnpj", "")
    ambiente = request.cookies.get("ambiente", "producao_restrita")
    cert_tipo = request.cookies.get("cert_tipo", "A1")

    periodo = f"{ano_ini:04d}-{mes_ini:02d}..{ano_fim:04d}-{mes_fim:02d}"

    eventos = expandir_temas(temas)
    ws = WSEsocialAdapter(cnpj, ambiente)
    retorno = ws.executar(eventos, periodo)

    resultado = {"eventos_executados": eventos, "retorno": retorno}

    return templates.TemplateResponse(
        "checklist.html",
        {"request": request, "cnpj": cnpj, "ambiente": ambiente, "cert_tipo": cert_tipo, "resultado": resultado},
    )