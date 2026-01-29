from src.services.ws_adapter import WSEsocialAdapter

ws = WSEsocialAdapter("00000000000000", "producao_restrita")
print(ws.executar(["S-2200", "S-1200", "S-1210"], "2025-01..2025-12"))