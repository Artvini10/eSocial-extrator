# eSocial Extractor - Copilot Instructions

## Project Overview
**eSocial Extractor** is a FastAPI-based tool that orchestrates the extraction, transformation, and submission of Brazilian labor/HR data to the eSocial platform. It integrates RPA (browser automation via Playwright), government web services, and data transformation pipelines.

## Architecture Overview

### Three-Tier Data Flow
1. **RPA Adapter** ([src/services/rpa_adapter.py](src/services/rpa_adapter.py)): Playwright-based browser automation against gov.br (stores auth state in `.auth/{cnpj}.json`)
2. **Orchestrator** ([src/services/orchestrator.py](src/services/orchestrator.py)): Maps "temas" (HR topics) to eSocial event codes using [config/events_supported.yaml](config/events_supported.yaml)
3. **Web Services Adapter** ([src/services/ws_adapter.py](src/services/ws_adapter.py)): Submits XML batches to eSocial API, polls for async results

### Configuration & Routing
- **Events Mapping**: [config/events_supported.yaml](config/events_supported.yaml) - defines tema→evento mappings (e.g., "Funcionário" → S-2190, S-2200, etc.)
- **Web Routes**: [src/routes/onboarding.py](src/routes/onboarding.py) - serves HTML templates for access (`/`) and checklist (`/checklist`)
- **Client Config**: [config/clients.yaml](config/clients.yaml) - certificates and credentials (currently empty, needs structure)

### Data Processing Pipeline
- **Writer** ([src/load/writer.py](src/load/writer.py)): Exports pandas DataFrames to Excel with current/historical splits (`*_ATUAL.xlsx`, `*_HISTORICO.xlsx`)
- **Writer Pack** ([src/load/writer_pack.py](src/load/writer_pack.py)): Generates ZIP packages containing Excel sheets and `metadata.json` using `gerar_pacote_outputs()` (used by background jobs)
- **Lineage** ([src/services/lineage.py](src/services/lineage.py)): Applies event versioning and current-flag logic - `isAtual` marks latest version per event ID
- **Logging**: Structured logs via `structlog` (setup in [src/common/logging_setup.py](src/common/logging_setup.py) - currently empty)

## Key Patterns & Conventions

### Error Handling
Custom error class ([src/common/errors.py](src/common/errors.py)): `ErroExplicado` with `causa` and `solucao` fields for better user messaging.

### Event Code Mapping Logic
Orchestrator uses YAML to expand theme-based queries:
```python
# temas = ["Funcionário", "Dependentes"]
# Returns: ["S-2190", "S-2200", "S-2205", ...]
orchestrator.expand(temas)
```

### DataFrame Versioning Pattern
Events have multiple versions tracked by `dtRecepcao`/`nrRecibo`, with `isAtual` flag marking the latest:
```python
# Sort by date, group by event ID, mark max version
aplicar_historico(df)
```

### Authentication via Playwright
Auth state persisted per CNPJ: `.auth/{cnpj}.json` - supports resuming browser sessions.

## Development Workflow

### Dependencies
Key tech stack (see [requirements.txt](requirements.txt)):
- **FastAPI + Uvicorn** - REST API server
- **Playwright** - RPA automation (headless=False for debugging)
- **httpx** - Async HTTP with SSL cert auth
- **pandas + openpyxl** - Data transformation & Excel export
- **pyyaml + lxml** - Config & XML parsing
- **signxml + cryptography** - Digital signatures (eSocial requirement)
- **structlog + rich** - Logging & CLI output

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server (dev mode)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Key Extension Points
1. **New HR Themes**: Add tema→eventos mapping to [config/events_supported.yaml](config/events_supported.yaml)
2. **New Routes**: Extend [src/routes/onboarding.py](src/routes/onboarding.py) following FastAPI templating pattern
3. **Custom Transformations**: Implement in [src/transform/](src/transform/) (currently empty)
4. **Error Scenarios**: Use `ErroExplicado` for structured error reporting

## Recent Updates (January 2026)

### Output Package Generation
- **Writer Pack Module** ([src/load/writer_pack.py](src/load/writer_pack.py)): Generates ZIP archives containing Excel sheets and metadata
  - Current (`_ATUAL.xlsx`) and historical (`_HISTORICO.xlsx`) splits per theme
  - Normalized columns: `evento`, `periodo`, `statusProc`, `nrRecibo`, `isAtual`, `versao`, `dtRecepcao`
  - `execucao.json` metadata audit file
  - Graceful fallback when transform layer unavailable
- **Transform Integration**: Supports `normalizar_funcionarios()` + `aplicar_lineage_simplificado()` from [src/transform/funcionarios.py](src/transform/funcionarios.py)

### Background Job System
- **Job Lifecycle** ([src/services/jobs.py](src/services/jobs.py)): In-memory job store with background execution
- **POST /executar Enhancements**:
  - Async handler for concurrency
  - Backward-compatible field names: `ano_inicial`/`ano_ini`, `ano_final`/`ano_fim`, `temas`/`processos`
  - Raw form parsing for flexibility
  - Progress tracking: EXECUTANDO → CONCLUIDO (0-100%)
  - ZIP package generation via `gerar_pacote_outputs()`

### Test Status
✅ **All Tests Passing**: Project imports, FastAPI routes, templates, configuration, server startup (port 8000)

## Important Notes
- **eSocial API Polling**: `ws_adapter.consultar()` expects hardcoded sleep - should be replaced with exponential backoff
- **Transform Layer**: [src/transform/](src/transform/) is empty and ready for data mapping logic
- **Config Gaps**: [config/clients.yaml](config/clients.yaml) needs schema definition for certificates and credentials
- **AI Helper**: [src/common/ai_helper.py](src/common/ai_helper.py) is empty - intended for LLM-assisted transformations
- **Logging Setup**: [src/common/logging_setup.py](src/common/logging_setup.py) needs structlog configuration
- **Lineage Integration**: [src/services/lineage.py](src/services/lineage.py) provides versioning; new `writer_pack` integrates it for output generation
