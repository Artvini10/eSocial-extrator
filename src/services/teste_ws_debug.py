from src.services.ws_adapter import WSEsocialAdapter

ambiente = "producao_restrita"
cnpj = "00000000000000"

ws = WSEsocialAdapter(cnpj, ambiente)

try:
    r = ws.session.get(ws.envio_url + "?wsdl", timeout=30)
    print("STATUS:", r.status_code)
    print("HEADERS:", dict(r.headers))
    print("BODY (inicio):", r.text[:300])
finally:
    ws.close()