import time
from typing import Any

import requests
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn

from .mtls_client import criar_sessao_mtls_de_pfx, MTLSContext
from .ws_config import carregar_ws_config
from .ws_simulador import WSEsocialSimulador


class WSEsocialAdapter:
    def __init__(self, cnpj: str, ambiente: str):
        self.cnpj = cnpj
        self.ambiente = ambiente

        cfg = carregar_ws_config(ambiente)
        self.envio_url = cfg.envio_url
        self.consulta_url = cfg.consulta_url
        self.simulacao = cfg.simulacao

        self._mtls: MTLSContext | None = None
        self.session: requests.Session | None = None

        if not self.simulacao:
            self._mtls = criar_sessao_mtls_de_pfx(
                pfx_path=cfg.cert_path,
                password=cfg.cert_password,
                ca_bundle_path=cfg.ca_bundle_path,
            )
            self.session = self._mtls.session

        self._sim = WSEsocialSimulador()

    def close(self) -> None:
        if self._mtls:
            self._mtls.close()

    def ping_wsdl(self) -> dict[str, int]:
        if self.simulacao:
            return {"envio_wsdl": 200, "consulta_wsdl": 200}

        assert self.session is not None
        try:
            r1 = self.session.get(self.envio_url + "?wsdl", timeout=30)
            r2 = self.session.get(self.consulta_url + "?wsdl", timeout=30)
            return {"envio_wsdl": r1.status_code, "consulta_wsdl": r2.status_code}
        finally:
            self.close()

    def executar(self, eventos: list[str], periodo: str) -> dict[str, Any]:
        """
        Fluxo:
        1) Envia lote (recebe protocolo + tempoEstimadoConclusao)
        2) Aguarda tempo estimado
        3) Consulta lote até concluir (sem martelar)
        """
        try:
            if self.simulacao:
                envio = self._sim.enviar_lote(self.cnpj, eventos, periodo)
            else:
                # Próximo passo quando tiver A1 real: montar SOAP e chamar envio_url.
                # Por enquanto, explicitamos que não está habilitado sem cert válido.
                raise RuntimeError("SIMULACAO=false, mas integração SOAP real ainda não foi habilitada sem certificado ICP-Brasil.")

            protocolo = envio["protocolo"]
            tempo_estimado = int(envio.get("tempoEstimadoConclusaoSeg", 3))

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.completed}/{task.total}"),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task("Processando lote (simulação)", total=max(tempo_estimado, 1))

                for _ in range(tempo_estimado):
                    time.sleep(1)
                    progress.update(task, advance=1)

                while True:
                    consulta = self._sim.consultar_lote(protocolo)
                    if consulta["status"] == "PROCESSANDO":
                        time.sleep(1)
                        continue
                    break

            return {
                "modo": "SIMULACAO" if self.simulacao else "WS",
                "envio": envio,
                "consulta": consulta,
            }
        finally:
            self.close()