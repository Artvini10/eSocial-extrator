from pathlib import Path
from datetime import datetime
import pandas as pd


def salvar_resultado_excel(payload: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = out_dir / f"resultado_extracao_{ts}.xlsx"

    eventos = payload.get("eventos_executados") or payload.get("eventos_executados", [])
    retorno = payload.get("retornos") or payload.get("retorno") or {}

    envio = retorno.get("envio", {})
    consulta = retorno.get("consulta", {})
    resultados = consulta.get("resultados", [])

    df_resultados = pd.DataFrame(resultados)
    df_envio = pd.DataFrame([envio])
    df_meta = pd.DataFrame([{
        "modo": retorno.get("modo", ""),
        "status_envio": envio.get("status", ""),
        "protocolo": envio.get("protocolo", ""),
        "tempoEstimadoConclusaoSeg": envio.get("tempoEstimadoConclusaoSeg", ""),
        "status_consulta": consulta.get("status", ""),
        "qtd_eventos": len(eventos),
    }])

    with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:
        df_meta.to_excel(writer, index=False, sheet_name="META")
        df_envio.to_excel(writer, index=False, sheet_name="ENVIO")
        df_resultados.to_excel(writer, index=False, sheet_name="RESULTADOS")

    return arquivo