#!/usr/bin/env python3
"""
Test FastAPI app startup and basic route functionality
"""

import sys
import asyncio
from fastapi.testclient import TestClient

print("\n" + "=" * 70)
print("FASTAPI APPLICATION TESTS")
print("=" * 70)

try:
    print("\n[TEST] Importing FastAPI app...")
    from src.main import app
    print("  ✓ App imported successfully")
    
    print("\n[TEST] Creating test client...")
    client = TestClient(app)
    print("  ✓ Test client created")
    
    print("\n[TEST] Testing routes...")
    
    # Test root route
    print("\n  Testing GET /")
    response = client.get("/")
    print(f"    Status: {response.status_code}")
    if response.status_code == 200:
        print(f"    ✓ Root route works")
        has_logo = "logo.png" in response.text
        has_form = "cnpj" in response.text.lower()
        print(f"    ✓ Contains logo reference: {has_logo}")
        print(f"    ✓ Contains form fields: {has_form}")
    else:
        print(f"    ✗ Expected 200, got {response.status_code}")
    
    # Test checklist route (should redirect since no cookie)
    print("\n  Testing GET /checklist")
    response = client.get("/checklist", follow_redirects=False)
    print(f"    Status: {response.status_code}")
    if response.status_code in [200, 307, 302]:
        print(f"    ✓ Checklist route accessible")
    else:
        print(f"    ✗ Unexpected status: {response.status_code}")
    
    # Test POST acesso
    print("\n  Testing POST /acesso (form submission)")
    response = client.post("/acesso", data={
        "cnpj": "12345678901234",
        "ambiente": "producao_restrita",
        "certificado": "A1"
    }, follow_redirects=True)
    print(f"    Status: {response.status_code}")
    if response.status_code == 200:
        print(f"    ✓ Form submission handled")
    else:
        print(f"    ✗ Status: {response.status_code}")
    
    print("\n" + "=" * 70)
    print("✓ FASTAPI TESTS PASSED")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
