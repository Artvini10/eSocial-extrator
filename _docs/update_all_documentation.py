"""
Master Documentation Updater
Synchronizes both English and Portuguese documentation with current codebase.

Usage: python update_all_documentation.py
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def run_update_script(script_name):
    """Execute an update script."""
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
        if result.stderr and "warning" not in result.stderr.lower():
            print(result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Timeout executing {script_name}")
        return False
    except Exception as e:
        print(f"[ERROR] Error executing {script_name}: {e}")
        return False


def main():
    """Update all documentation files."""
    print("\n" + "="*70)
    print("[MASTER] DOCUMENTATION UPDATER")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    success_count = 0
    total_count = 2
    
    # Update English documentation
    print("Step 1/2: Updating English documentation...")
    print("-" * 70)
    if run_update_script("update_documentation_en.py"):
        success_count += 1
    
    print()
    
    # Update Portuguese documentation
    print("Step 2/2: Updating Portuguese documentation...")
    print("-" * 70)
    if run_update_script("update_documentation_ptbr.py"):
        success_count += 1
    
    # Final summary
    print("\n" + "="*70)
    print("UPDATE SUMMARY")
    print("="*70)
    print(f"[OK] Successful: {success_count}/{total_count}")
    print(f"[ERROR] Failed: {total_count - success_count}/{total_count}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    if success_count == total_count:
        print("[OK] All documentation files updated successfully!")
        return 0
    else:
        print("[WARNING] Some documentation files failed to update.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
