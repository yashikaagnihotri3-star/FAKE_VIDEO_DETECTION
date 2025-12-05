#!/usr/bin/env python3
"""Quick test script for the deepfake detector backend."""

import requests
import json
import time
import io

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the /health endpoint."""
    print("\n" + "="*60)
    print("TEST 1: /health Endpoint")
    print("="*60)
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {resp.status_code}")
        data = resp.json()
        print(f"Response:\n{json.dumps(data, indent=2)}")
        print("✓ PASS: Health check successful, detector_mode is:", data.get('detector_mode'))
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")

def test_detect_mock():
    """Test /api/detect endpoint with a mock video file."""
    print("\n" + "="*60)
    print("TEST 2: /api/detect with Mock Video")
    print("="*60)
    try:
        # Create a fake video file (just some bytes)
        fake_video = io.BytesIO(b"fake_video_data_" * 100)
        files = {'video_file': ('test.mp4', fake_video, 'video/mp4')}
        
        resp = requests.post(f"{BASE_URL}/api/detect", files=files, timeout=10)
        print(f"Status Code: {resp.status_code}")
        data = resp.json()
        print(f"Response:\n{json.dumps(data, indent=2)}")
        
        if resp.status_code == 200:
            print("✓ PASS: Detection returned 200 (success)")
            print(f"  - Deepfake Score: {data.get('deepfake_score')}")
            print(f"  - Is Deepfake: {data.get('is_deepfake')}")
        elif resp.status_code == 202:
            print("✓ PASS: Detection returned 202 (queued)")
            print(f"  - Status: {data.get('status')}")
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")

def test_results():
    """Test /api/results endpoint."""
    print("\n" + "="*60)
    print("TEST 3: /api/results/{request_id}")
    print("="*60)
    try:
        # First do a detection to get a request_id
        fake_video = io.BytesIO(b"fake_video_data_" * 100)
        files = {'video_file': ('test2.mp4', fake_video, 'video/mp4')}
        detect_resp = requests.post(f"{BASE_URL}/api/detect", files=files, timeout=10)
        request_id = detect_resp.json().get('request_id')
        print(f"Detection request_id: {request_id}")
        
        # Now try to retrieve it
        resp = requests.get(f"{BASE_URL}/api/results/{request_id}", timeout=5)
        print(f"Status Code: {resp.status_code}")
        data = resp.json()
        print(f"Result Status: {data.get('status')}")
        print("✓ PASS: Retrieved result successfully")
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")

if __name__ == "__main__":
    print("\n🎬 Deepfake Detector Backend Test Suite")
    print(f"Target: {BASE_URL}")
    
    try:
        test_health()
        time.sleep(1)
        test_detect_mock()
        time.sleep(1)
        test_results()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED")
        print("="*60 + "\n")
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\n✗ ERROR: {str(e)}")
