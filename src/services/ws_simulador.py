import time
import uuid
from dataclasses import dataclass
from typing import Any

@dataclass
class LoteSimulado:
    protocolo: str
    criado_em: float
    tempo_estimado_seg: int
    payload: dict[str, Any]

class WSEsocialSimulador:
    def __init__(self) -> None:
        self._lotes: dict[str, LoteSimulado] = {}

    def enviar_lote(self, cnpj: str, eventos: list[str], periodo: str) -> dict[str, Any]:
        protocolo = str(uuid.uuid4())
        tempo_estimado_seg = 3  # simula tempoEstimadoConclusao
        lote = LoteSimulado(
            protocolo=protocolo,
            criado_em=time.time(),
            tempo_estimado_seg=tempo_estimado_seg,
            payload={
                "cnpj": cnpj,
                "eventos": eventos,
                "periodo": periodo,
            },
        )
        self._lotes[protocolo] = lote
        return {
            "protocolo": protocolo,
            "tempoEstimadoConclusaoSeg": tempo_estimado_seg,
            "status": "RECEBIDO",
        }

    def consultar_lote(self, protocolo: str) -> dict[str, Any]:
        if protocolo not in self._lotes:
            return {"status": "NAO_ENCONTRADO", "protocolo": protocolo}

        lote = self._lotes[protocolo]
        decorrido = time.time() - lote.criado_em

        if decorrido < lote.tempo_estimado_seg:
            return {
                "status": "PROCESSANDO",
                "protocolo": protocolo,
                "tempoRestanteSeg": int(lote.tempo_estimado_seg - decorrido),
            }

        # simula retorno “finalizado”
        return {
            "status": "CONCLUIDO",
            "protocolo": protocolo,
            "resultados": [
                {"evento": ev, "periodo": lote.payload["periodo"], "statusProc": "SUCESSO", "nrRecibo": f"REC-{uuid.uuid4().hex[:10]}"} 
                for ev in lote.payload["eventos"]
            ],
        }