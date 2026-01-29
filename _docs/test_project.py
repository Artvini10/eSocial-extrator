#!/usr/bin/env python3
"""
Comprehensive test suite for eSocial Extractor project
Tests all imports, configurations, and core functionality
"""

import sys
import os
from pathlib import Path

# Change to project root
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

print("=" * 70)
print("COMPREHENSIVE PROJECT TEST SUITE")
print(f"Project root: {PROJECT_ROOT}")
print("=" * 70)
print("=" * 70)

# Test 1: Imports
print("\n[TEST 1] Testing Critical Imports...")
print("-" * 70)

imports_to_test = [
    ("FastAPI", "from fastapi import FastAPI"),
    ("Main app", "from src.main import app"),
    ("Routes", "from src.routes.onboarding import router"),
    ("Orchestrator", "from src.services.orchestrator import expandir_temas"),
    ("WS Adapter", "from src.services.ws_adapter import WSEsocialAdapter"),
    ("WS Simulador", "from src.services.ws_simulador import WSEsocialSimulador"),
    ("Lineage", "from src.services.lineage import aplicar_historico"),
    ("Errors", "from src.common.errors import ErroExplicado"),
    ("Writer", "from src.load.writer import salvar_resultado_excel"),
    ("MTLS Client", "from src.services.mtls_client import criar_sessao_mtls_de_pfx"),
    ("XML Signer", "from src.services.xml_signer import assinar_xml"),
    ("Cert Manager", "from src.services.cert_manager import carregar_certificado_pfx"),
]

import_errors = []
for name, import_stmt in imports_to_test:
    try:
        exec(import_stmt)
        print(f"  ✓ {name:25} - OK")
    except Exception as e:
        error_msg = str(e)[:60]
        print(f"  ✗ {name:25} - ERROR: {error_msg}")
        import_errors.append((name, str(e)))

# Test 2: Config Files
print("\n[TEST 2] Validating Configuration Files...")
print("-" * 70)

import yaml
config_files = {
    "config/events_supported.yaml": "Event mappings",
    ".env.example": "Environment template",
}

config_errors = []
for config_path, description in config_files.items():
    if Path(config_path).exists():
        try:
            if config_path.endswith(".yaml"):
                with open(config_path) as f:
                    data = yaml.safe_load(f)
                    if data:
                        print(f"  ✓ {config_path:35} ({description}) - Valid")
                    else:
                        print(f"  ⚠ {config_path:35} ({description}) - Empty")
            else:
                print(f"  ✓ {config_path:35} ({description}) - Exists")
        except Exception as e:
            print(f"  ✗ {config_path:35} - ERROR: {str(e)[:40]}")
            config_errors.append((config_path, str(e)))
    else:
        print(f"  ⚠ {config_path:35} - Not found (optional)")

# Test 3: Key Functions
print("\n[TEST 3] Testing Core Functions...")
print("-" * 70)

function_errors = []

# Test orchestrator
try:
    from src.services.orchestrator import expandir_temas
    result = expandir_temas([])  # Empty list should return []
    if result == []:
        print(f"  ✓ expandir_temas([])           - Returns empty list")
    else:
        print(f"  ✗ expandir_temas([])           - Expected [], got {result}")
        function_errors.append(("expandir_temas", f"Expected [], got {result}"))
except Exception as e:
    print(f"  ✗ expandir_temas()             - ERROR: {str(e)[:40]}")
    function_errors.append(("expandir_temas", str(e)))

# Test lineage
try:
    from src.services.lineage import aplicar_historico
    import pandas as pd
    test_df = pd.DataFrame({
        "dtRecepcao": ["2025-01-01", "2025-01-02"],
        "nrRecibo": ["123", "124"],
        "idEvento": ["S-2200", "S-2200"],
    })
    result_df = aplicar_historico(test_df)
    if "isAtual" in result_df.columns and "versao" in result_df.columns:
        print(f"  ✓ aplicar_historico()          - Adds versao and isAtual columns")
    else:
        print(f"  ✗ aplicar_historico()          - Missing expected columns")
        function_errors.append(("aplicar_historico", "Missing columns"))
except Exception as e:
    print(f"  ✗ aplicar_historico()          - ERROR: {str(e)[:40]}")
    function_errors.append(("aplicar_historico", str(e)))

# Test error class
try:
    from src.common.errors import ErroExplicado
    erro = ErroExplicado("Test message", "Test cause", "Test solution")
    if erro.causa == "Test cause" and erro.solucao == "Test solution":
        print(f"  ✓ ErroExplicado                - Proper structure")
    else:
        print(f"  ✗ ErroExplicado                - Missing attributes")
        function_errors.append(("ErroExplicado", "Missing attributes"))
except Exception as e:
    print(f"  ✗ ErroExplicado                - ERROR: {str(e)[:40]}")
    function_errors.append(("ErroExplicado", str(e)))

# Test 4: Static Files
print("\n[TEST 4] Checking Static Assets...")
print("-" * 70)

static_files = {
    "src/static/logo.png": "Logo",
    "src/static/style.css": "Stylesheet",
}

asset_errors = []
for asset_path, description in static_files.items():
    if Path(asset_path).exists():
        size = Path(asset_path).stat().st_size
        print(f"  ✓ {asset_path:35} ({description:15}) - {size} bytes")
    else:
        print(f"  ✗ {asset_path:35} ({description:15}) - NOT FOUND")
        asset_errors.append(asset_path)

# Test 5: Template Files
print("\n[TEST 5] Checking Templates...")
print("-" * 70)

templates = ["src/templates/acesso.html", "src/templates/checklist.html"]

template_errors = []
for template_path in templates:
    if Path(template_path).exists():
        with open(template_path, encoding='utf-8', errors='ignore') as f:
            content = f.read()
            size = len(content)
            has_logo = "logo.png" in content
            print(f"  ✓ {template_path:35} - {size} bytes, logo ref: {has_logo}")
    else:
        print(f"  ✗ {template_path:35} - NOT FOUND")
        template_errors.append(template_path)

# Test 6: Directory Structure
print("\n[TEST 6] Verifying Directory Structure...")
print("-" * 70)

expected_dirs = [
    "src/services",
    "src/routes",
    "src/common",
    "src/load",
    "src/transform",
    "src/static",
    "src/templates",
    "config",
    ".github",
]

dir_errors = []
for dir_path in expected_dirs:
    if Path(dir_path).exists():
        print(f"  ✓ {dir_path:35} - OK")
    else:
        print(f"  ✗ {dir_path:35} - MISSING")
        dir_errors.append(dir_path)

# Test 7: Package __init__ files
print("\n[TEST 7] Checking Package Structure (__init__.py)...")
print("-" * 70)

init_files = [
    "src/__init__.py",
    "src/services/__init__.py",
    "src/routes/__init__.py",
    "src/common/__init__.py",
    "src/load/__init__.py",
    "src/transform/__init__.py",
]

init_errors = []
for init_file in init_files:
    if Path(init_file).exists():
        print(f"  ✓ {init_file:35} - OK")
    else:
        print(f"  ✗ {init_file:35} - MISSING")
        init_errors.append(init_file)

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

total_errors = (
    len(import_errors)
    + len(config_errors)
    + len(function_errors)
    + len(asset_errors)
    + len(template_errors)
    + len(dir_errors)
    + len(init_errors)
)

print(f"Import Errors:       {len(import_errors)}")
print(f"Config Errors:       {len(config_errors)}")
print(f"Function Errors:     {len(function_errors)}")
print(f"Asset Errors:        {len(asset_errors)}")
print(f"Template Errors:     {len(template_errors)}")
print(f"Directory Errors:    {len(dir_errors)}")
print(f"Init File Errors:    {len(init_errors)}")
print("-" * 70)
print(f"TOTAL ERRORS:        {total_errors}")

if total_errors == 0:
    print("\n✓ ALL TESTS PASSED - Project is ready!")
    sys.exit(0)
else:
    print(f"\n✗ {total_errors} ERRORS FOUND - See details above")
    sys.exit(1)
