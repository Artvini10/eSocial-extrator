from pathlib import Path
import yaml

EVENTS_FILE = Path("config/events_supported.yaml")

def carregar_eventos():
    if not EVENTS_FILE.exists():
        raise FileNotFoundError(f"Arquivo {EVENTS_FILE} não encontrado. Verifique a configuração.")
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        eventos_map = yaml.safe_load(f)
        if not eventos_map:
            raise ValueError(f"Arquivo {EVENTS_FILE} vazio ou inválido")
        return eventos_map

def expandir_temas(temas_selecionados: list[str]) -> list[str]:
    if not temas_selecionados:
        return []
    
    eventos = carregar_eventos()
    eventos_finais = set()

    for tema in temas_selecionados:
        if tema not in eventos:
            raise ValueError(f"Tema '{tema}' não mapeado em events_supported.yaml")
        eventos_finais.update(eventos.get(tema, []))

    return sorted(eventos_finais)
