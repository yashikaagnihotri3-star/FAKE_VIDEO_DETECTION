#!/usr/bin/env python3
"""
Simple test script to verify API is working
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_home():
    """Test home endpoint"""
    print("\nTesting / endpoint...")
    try:
        response = requests.get(BASE_URL)
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response length: {len(response.text)} bytes")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_file(file_path):
    """Test detection with file"""
    print(f"\nTesting /api/detect with file: {file_path}")
    
    import os
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, "rb") as f:
            files = {"video_file": f}
            response = requests.post(f"{BASE_URL}/api/detect", files=files)
        
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 API Test Suite")
    print("=" * 50)
    
    results = {
        "Health": test_health(),
        "Home": test_home(),
    }
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")

if __name__ == "__main__":
    main()
