from fastapi.responses import RedirectResponse, JSONResponse
from src.services.jobs import criar_job, rodar_em_background, get_job, atualizar
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.services.orchestrator import expandir_temas
from src.services.ws_adapter import WSEsocialAdapter
from src.load.writer import salvar_resultado_excel
from src.services.jobs import criar_job, rodar_em_background, get_job, atualizar

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


@router.post("/executar")
def executar_async(
    request: Request,
    cnpj: str = Form(...),
    ambiente: str = Form(...),
    certificado: str = Form(...),
    ano_inicial: int = Form(...),
    ano_final: int = Form(...),
    processos: list[str] = Form(default=[]),
):
    if not processos:
        return templates.TemplateResponse(
            "resultado.html",
            {"request": request, "ok": False, "erro": "Selecione pelo menos 1 processo."},
            status_code=400,
        )

    job = criar_job()

    periodo = f"{ano_inicial}-01..{ano_final}-12"
    eventos = expandir_temas(processos)

    def _task(job_id: str):
        atualizar(job_id, progress=5, message="Expandindo temas...")
        ws = WSEsocialAdapter(cnpj, ambiente)

        atualizar(job_id, progress=20, message="Executando WS (lote/consulta)...")
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

        atualizar(job_id, progress=80, message="Gerando Excel...")
        arquivo = salvar_resultado_excel(payload, OUTPUTS_DIR)

        atualizar(
            job_id,
            status="CONCLUIDO",
            progress=100,
            message="Concluído.",
            result=payload,
            output_file=arquivo.name,
        )

    rodar_em_background(job.job_id, _task)

    return RedirectResponse(url=f"/status/{job.job_id}", status_code=303)


@router.get("/download/{nome_arquivo}")
def download(nome_arquivo: str):
    arquivo = OUTPUTS_DIR / nome_arquivo
    if not arquivo.exists():
        return {"ok": False, "erro": "Arquivo não encontrado."}
    return FileResponse(path=str(arquivo), filename=nome_arquivo)


@router.post("/jobs", response_class=JSONResponse)
def criar_job_endpoint():
    """Create a new job and return its id."""
    job = criar_job()
    return JSONResponse({"ok": True, "job_id": job.job_id, "status": job.status})


@router.post("/jobs/run", response_class=JSONResponse)
def criar_e_executar_job(
    request: Request,
    ano_ini: int = Form(...),
    mes_ini: int = Form(...),
    ano_fim: int = Form(...),
    mes_fim: int = Form(...),
    temas: list[str] = Form(default=[]),
):
    """Create a job and run the extraction in background using same logic as /executar."""
    if not temas:
        return JSONResponse({"ok": False, "erro": "Selecione pelo menos 1 tema."}, status_code=400)

    cnpj = request.cookies.get("cnpj", "")
    ambiente = request.cookies.get("ambiente", "producao_restrita")
    certificado = request.cookies.get("certificado", "A1")

    periodo = f"{ano_ini:04d}-{mes_ini:02d}..{ano_fim:04d}-{mes_fim:02d}"
    eventos = expandir_temas(temas)

    job = criar_job()

    def _job_fn(job_id_local, cnpj_local, ambiente_local, certificado_local, periodo_local, eventos_local):
        try:
            atualizar(job_id_local, status="RODANDO", progress=5, message="Iniciando execução")
            ws = WSEsocialAdapter(cnpj_local, ambiente_local)
            retorno = ws.executar(eventos_local, periodo_local)

            payload = {
                "cnpj": cnpj_local,
                "ambiente": ambiente_local,
                "certificado": certificado_local,
                "periodo": periodo_local,
                "temas": eventos_local,
                "eventos_executados": eventos_local,
                "retornos": retorno,
            }

            arquivo = salvar_resultado_excel(payload, OUTPUTS_DIR)
            atualizar(job_id_local, status="CONCLUIDO", progress=100, result={"arquivo": arquivo.name}, output_file=str(arquivo), message="Concluído")
        except Exception as e:
            atualizar(job_id_local, status="ERRO", error=str(e), message="Falha na execução", progress=100)

    rodar_em_background(job.job_id, _job_fn, cnpj, ambiente, certificado, periodo, eventos)

    return JSONResponse({"ok": True, "job_id": job.job_id, "status": job.status})


@router.get("/jobs/{job_id}", response_class=JSONResponse)
def consultar_job(job_id: str):
    st = get_job(job_id)
    if not st:
        return JSONResponse({"ok": False, "erro": "Job não encontrado."}, status_code=404)
    # convert dataclass to dict
    data = {
        "job_id": st.job_id,
        "created_at": st.created_at,
        "status": st.status,
        "progress": st.progress,
        "message": st.message,
        "result": st.result,
        "output_file": st.output_file,
        "error": st.error,
    }
    return JSONResponse({"ok": True, "job": data})

@router.get("/status/{job_id}", response_class=HTMLResponse)
def status_page(request: Request, job_id: str):
    st = get_job(job_id)
    if not st:
        return templates.TemplateResponse(
            "resultado.html",
            {"request": request, "ok": False, "erro": "JOB não encontrado."},
            status_code=404,
        )
    return templates.TemplateResponse(
        "status.html",
        {"request": request, "job_id": job_id},
    )


@router.get("/api/status/{job_id}")
def status_api(job_id: str):
    st = get_job(job_id)
    if not st:
        return JSONResponse({"ok": False, "erro": "JOB não encontrado."}, status_code=404)

    return {
        "ok": True,
        "job_id": st.job_id,
        "status": st.status,
        "progress": st.progress,
        "message": st.message,
        "error": st.error,
        "output_file": st.output_file,
        "result": st.result if st.status == "CONCLUIDO" else None,
    }
