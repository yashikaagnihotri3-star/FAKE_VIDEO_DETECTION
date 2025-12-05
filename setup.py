#!/usr/bin/env python3
"""
Installation Script - Simpler version without setup.py conflicts
"""

import os
import sys
import subprocess
from pathlib import Path

print("\n" + "="*60)
print("🚀 DEEPFAKE DETECTOR - INSTALLATION")
print("="*60)

# Check Python version
print(f"\n📌 Python Version: {sys.version}")
if sys.version_info < (3, 8):
    print("❌ Error: Python 3.8+ required!")
    sys.exit(1)

# Create directories
print("\n📂 Creating directories...")
Path("logs").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)
Path("results").mkdir(exist_ok=True)
print("✓ Directories created: logs, uploads, results")

# Check .env file
print("\n📝 Checking .env file...")
if not Path(".env").exists():
    print("⚠️  .env file not found!")
else:
    print("✓ .env file found")

# Install dependencies
print("\n📦 Installing dependencies (this may take a minute)...")
result = subprocess.run("pip install -r requirements_prod.txt", shell=True)

if result.returncode != 0:
    print("❌ Installation failed!")
    sys.exit(1)

print("✓ Dependencies installed!")

# Verify imports
print("\n🧪 Verifying installation...")
try:
    import fastapi
    import uvicorn
    import requests
    from dotenv import load_dotenv
    print("✓ All packages imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Check API key
print("\n🔑 Checking API key...")
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
if api_key:
    print("✓ API_KEY found in .env")
else:
    print("⚠️  API_KEY not found in .env - detection will fail")

print("\n" + "="*60)
print("✅ INSTALLATION COMPLETE!")
print("="*60)
print("""
Next steps:
1. Run: python run.py
2. Open: c:\\Users\\yashi\\OneDrive\\Desktop\\deepfake-detector\\index.html
3. Upload videos and analyze!

Ready to start? 🚀
""")
