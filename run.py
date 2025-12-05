#!/usr/bin/env python3
"""
Run this script to start the production backend server
With monitoring, logging, and health checks
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_env():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("   Create .env with: API_KEY=your_key_here")
        sys.exit(1)
    print("✓ .env file found")

def check_dependencies():
    """Check if all dependencies are installed"""
    required = ["fastapi", "uvicorn", "requests", "dotenv"]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements_prod.txt")
        sys.exit(1)
    print("✓ All dependencies installed")

def start_server():
    """Start the server"""
    print("\n" + "="*60)
    print("🚀 STARTING DEEPFAKE DETECTOR BACKEND")
    print("="*60)
    print(f"Starting at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📍 Server Configuration:")
    print("   Host: 0.0.0.0")
    print("   Port: 8000")
    print("   Reload: Enabled")
    print("\n🌐 Access Points:")
    print("   Home:    http://localhost:8000")
    print("   API Doc: http://localhost:8000/docs")
    print("   Health:  http://localhost:8000/health")
    print("\n📝 Logs: ./logs/")
    print("📂 Results: ./results/")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    cmd = "uvicorn server_production:app --host 0.0.0.0 --port 8000 --reload"
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    check_env()
    check_dependencies()
    start_server()
