"""
Test imports for whale_agent.py dependencies
"""
print("Starting import test...")

try:
    print("Testing nice_funcs import...")
    from src import nice_funcs as n
    print("✅ nice_funcs imported successfully")
except Exception as e:
    print(f"❌ nice_funcs import failed: {str(e)}")

try:
    print("\nTesting nice_funcs_hl import...")
    from src import nice_funcs_hl as hl
    print("✅ nice_funcs_hl imported successfully")
except Exception as e:
    print(f"❌ nice_funcs_hl import failed: {str(e)}")

try:
    print("\nTesting MoonDevAPI import...")
    from src.agents.api import MoonDevAPI
    print("✅ MoonDevAPI imported successfully")
except Exception as e:
    print(f"❌ MoonDevAPI import failed: {str(e)}")

try:
    print("\nTesting BaseAgent import...")
    from src.agents.base_agent import BaseAgent
    print("✅ BaseAgent imported successfully")
except Exception as e:
    print(f"❌ BaseAgent import failed: {str(e)}")

print("\nImport test complete.")
