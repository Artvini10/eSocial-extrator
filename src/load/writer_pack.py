"""
Module for generating output packages (ZIP files) with extraction results.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple
import json
import zipfile
import pandas as pd

try:
    from src.transform.funcionarios import normalizar_funcionarios
    NORMALIZAR_FUNC_AVAILABLE = True
except ImportError:
    NORMALIZAR_FUNC_AVAILABLE = False

try:
    from src.services.lineage import aplicar_lineage_simplificado
    LINEAGE_AVAILABLE = True
except ImportError:
    LINEAGE_AVAILABLE = False


def _salvar_xlsx(df: pd.DataFrame, path: Path, sheet: str):
    """Helper to save DataFrame to Excel."""
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name=sheet)


def _normalizar_para_df(resultados: List[Dict[str, Any]], tema: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fallback: normalize results to DataFrames when new transform layer unavailable."""
    df_hist = pd.DataFrame(resultados)

    # Garantir colunas padrão
    for col in ["evento", "periodo", "statusProc", "nrRecibo"]:
        if col not in df_hist.columns:
            df_hist[col] = None

    # Colunas extras obrigatórias
    if "isAtual" not in df_hist.columns:
        df_hist["isAtual"] = True
    if "versao" not in df_hist.columns:
        df_hist["versao"] = 1
    if "dtRecepcao" not in df_hist.columns:
        df_hist["dtRecepcao"] = None
    if "indRetif" not in df_hist.columns:
        df_hist["indRetif"] = None
    if "origem" not in df_hist.columns:
        df_hist["origem"] = "WS"
    if "statusProc" not in df_hist.columns:
        df_hist["statusProc"] = None
    if "valid_from" not in df_hist.columns:
        df_hist["valid_from"] = None
    if "valid_to" not in df_hist.columns:
        df_hist["valid_to"] = None

    # ATUAL: por enquanto, como não temos reconciliação real ainda, mantém isAtual=True
    df_atual = df_hist[df_hist["isAtual"] == True].copy()

    # Ordenação básica
    cols_front = ["evento", "periodo", "statusProc", "nrRecibo", "isAtual", "versao", "dtRecepcao", "indRetif", "origem", "valid_from", "valid_to"]
    cols_front = [c for c in cols_front if c in df_hist.columns]
    rest = [c for c in df_hist.columns if c not in cols_front]
    df_hist = df_hist[cols_front + rest]
    df_atual = df_atual[cols_front + rest]

    return df_atual, df_hist


def gerar_pacote_outputs(payload: Dict[str, Any], out_dir: Path) -> Path:
    """
    Generate a ZIP package containing Excel and metadata files from extraction results.
    
    Args:
        payload: Dictionary with keys:
            - cnpj: CNPJ extracted
            - ambiente: Environment used
            - processos: List of themes processed
            - periodo: Period string (YYYY-MM..YYYY-MM)
            - retornos: eSocial API response data
        out_dir: Output directory for the ZIP file
    
    Returns:
        Path to the generated ZIP file
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    cnpj = payload.get("cnpj")
    ambiente = payload.get("ambiente")
    periodo = payload.get("periodo")
    processos = payload.get("processos", []) or []

    retornos = payload.get("retornos", {}) or {}
    consulta = retornos.get("consulta", {}) or {}
    resultados = consulta.get("resultados", []) or []

    gerados: List[Path] = []

    # --- Tema: Funcionários (se novo transform layer disponível) ---
    if NORMALIZAR_FUNC_AVAILABLE and LINEAGE_AVAILABLE:
        selecionou_func = any("Vínculos" in p or "Vínculos de Emprego" in p or "Funcion" in p for p in processos) or True

        if selecionou_func:
            try:
                rows = normalizar_funcionarios(resultados, cnpj, ambiente, periodo)
                chave = ["cnpj", "evento"]
                df_atual, df_hist = aplicar_lineage_simplificado(rows, chave_cols=chave)

                f_atual = out_dir / "Funcionarios_ATUAL.xlsx"
                f_hist = out_dir / "Funcionarios_HISTORICO.xlsx"

                _salvar_xlsx(df_atual, f_atual, "ATUAL")
                _salvar_xlsx(df_hist, f_hist, "HISTORICO")

                gerados.extend([f_atual, f_hist])
            except Exception as e:
                # Se falhar, cai para fallback
                print(f"Aviso: normalizar_funcionarios falhou ({e}), usando fallback.")
                pass

    # --- Fallback: usar _normalizar_para_df por tema ---
    if not gerados or not NORMALIZAR_FUNC_AVAILABLE:
        temas = processos[:] if processos else ["Exportacao"]

        for tema in temas:
            df_atual, df_hist = _normalizar_para_df(resultados, tema)

            nome_base = tema.replace(" ", "_")
            f_atual = out_dir / f"{nome_base}_ATUAL.xlsx"
            f_hist = out_dir / f"{nome_base}_HISTORICO.xlsx"

            _salvar_xlsx(df_atual, f_atual, "ATUAL")
            _salvar_xlsx(df_hist, f_hist, "HISTORICO")

            gerados.extend([f_atual, f_hist])

    # Auditoria
    audit = out_dir / "execucao.json"
    audit.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # ZIP final
    zip_path = out_dir / "resultado.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(audit, arcname=audit.name)
        for f in gerados:
            z.write(f, arcname=f.name)

    return zip_path
