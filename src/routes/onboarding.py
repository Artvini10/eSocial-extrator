from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.services.orchestrator import expandir_temas
from src.services.ws_adapter import WSEsocialAdapter
from src.load.writer import salvar_resultado_excel

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[1]  # .../src
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
OUTPUTS_DIR = BASE_DIR.parent / "outputs"


@router.get("/", response_class=HTMLResponse)
def acesso(request: Request):
    return templates.TemplateResponse(request, "acesso.html", {})


@router.post("/acesso", response_class=HTMLResponse)
def salvar_acesso(
    cnpj: str = Form(...),
    ambiente: str = Form(...),
    certificado: str = Form(...),
):
    resp = RedirectResponse(url="/checklist", status_code=303)
    resp.set_cookie("cnpj", cnpj, httponly=True, samesite="strict")
    resp.set_cookie("ambiente", ambiente, httponly=True, samesite="strict")
    resp.set_cookie("certificado", certificado, httponly=True, samesite="strict")
    return resp


@router.get("/checklist", response_class=HTMLResponse)
def checklist(request: Request):
    cnpj = request.cookies.get("cnpj", "")
    ambiente = request.cookies.get("ambiente", "producao_restrita")
    certificado = request.cookies.get("certificado", "A1")

    return templates.TemplateResponse(
        request, "checklist.html", {"cnpj": cnpj, "ambiente": ambiente, "certificado": certificado},
    )


@router.post("/executar", response_class=HTMLResponse)
def executar(
    request: Request,
    ano_inicial: int = Form(...),
    ano_final: int = Form(...),
    processos: list[str] = Form(default=[]),
):
    cnpj = request.cookies.get("cnpj", "")
    ambiente = request.cookies.get("ambiente", "producao_restrita")
    certificado = request.cookies.get("certificado", "A1")

    if not processos:
        return templates.TemplateResponse(
            request, "resultado.html", {"ok": False, "erro": "Selecione pelo menos 1 processo."},
            status_code=400,
        )

    periodo = f"{ano_inicial}-01..{ano_final}-12"
    eventos = expandir_temas(processos)

    ws = WSEsocialAdapter(cnpj, ambiente)
    retornos = ws.executar(eventos, periodo)

    payload = {
        "cnpj": cnpj,
        "ambiente": ambiente,
        "certificado": certificado,
        "periodo": periodo,
        "processos": processos,
        "eventos_executados": eventos,
        "retornos": retornos,
    }

    arquivo = salvar_resultado_excel(payload, OUTPUTS_DIR)
    nome_arquivo = arquivo.name

    return templates.TemplateResponse(
        request, "resultado.html",
        {
            "ok": True,
            "payload": payload,
            "arquivo": nome_arquivo,
        },
    )


@router.get("/download/{nome_arquivo}")
def download(nome_arquivo: str):
    arquivo = OUTPUTS_DIR / nome_arquivo
    if not arquivo.exists():
        return {"ok": False, "erro": "Arquivo não encontrado."}
    return FileResponse(path=str(arquivo), filename=nome_arquivo)