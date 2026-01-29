from src.services.ws_adapter import WSEsocialAdapter

ambiente = "producao_restrita"
cnpj = "00000000000000"

ws = WSEsocialAdapter(cnpj, ambiente)
print(ws.ping_wsdl())