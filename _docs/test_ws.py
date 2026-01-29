#!/usr/bin/env python3
"""
Test Web Services adapter and simulator functionality
"""

import sys

print("\n" + "=" * 70)
print("WEB SERVICES ADAPTER TESTS")
print("=" * 70)

try:
    from src.services.ws_simulador import WSEsocialSimulador
    from src.services.ws_adapter import WSEsocialAdapter
    from src.services.orchestrator import expandir_temas
    
    print("\n[TEST 1] Testing WS Simulador...")
    print("-" * 70)
    
    simulador = WSEsocialSimulador()
    print("  ✓ Simulador initialized")
    
    # Test enviar_lote
    envio_response = simulador.enviar_lote(
        cnpj="12345678901234",
        eventos=["S-2200", "S-1200"],
        periodo="2025-01..2025-12"
    )
    
    print(f"  ✓ enviar_lote() returns protocol: {envio_response.get('protocolo')[:8]}...")
    assert "protocolo" in envio_response
    assert "tempoEstimadoConclusaoSeg" in envio_response
    assert "status" in envio_response
    print(f"    - Status: {envio_response['status']}")
    print(f"    - Estimated time: {envio_response['tempoEstimadoConclusaoSeg']}s")
    
    # Test consultar_lote
    protocolo = envio_response["protocolo"]
    consulta_response = simulador.consultar_lote(protocolo)
    print(f"  ✓ consultar_lote() works")
    print(f"    - Status: {consulta_response['status']}")
    
    print("\n[TEST 2] Testing Orchestrator Theme Expansion...")
    print("-" * 70)
    
    # Test single theme
    eventos = expandir_temas(["Vinculos"])
    print(f"  ✓ expandir_temas(['Vinculos']) returns {len(eventos)} eventos")
    assert "S-2190" in eventos
    assert "S-2200" in eventos
    print(f"    - Sample eventos: {eventos[:3]}")
    
    # Test multiple themes
    eventos = expandir_temas(["Vinculos", "Dependentes"])
    print(f"  ✓ expandir_temas(['Vinculos', 'Dependentes']) returns {len(eventos)} eventos")
    
    # Test error handling
    print("\n[TEST 3] Testing Error Handling...")
    print("-" * 70)
    
    try:
        expandir_temas(["InvalidTema"])
        print("  ✗ Should have raised error for invalid tema")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓ Correctly raises ValueError for invalid tema")
        print(f"    - Error message: {str(e)[:50]}")
    
    print("\n[TEST 4] Testing WS Adapter (Simulacao mode)...")
    print("-" * 70)
    
    ws = WSEsocialAdapter(cnpj="12345678901234", ambiente="producao_restrita")
    print("  ✓ WS Adapter initialized in simulation mode")
    
    resultado = ws.executar(["S-2200", "S-1200"], "2025-01..2025-12")
    print(f"  ✓ executar() completes successfully")
    print(f"    - Mode: {resultado.get('modo')}")
    print(f"    - Envio status: {resultado['envio'].get('status')}")
    print(f"    - Consulta status: {resultado['consulta'].get('status')}")
    
    print("\n" + "=" * 70)
    print("✓ WEB SERVICES TESTS PASSED")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
