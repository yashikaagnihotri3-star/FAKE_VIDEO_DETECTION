#!/usr/bin/env python3
"""
Standalone deepfake detection script
Upload a video to Reality Defender API and get detection results
"""

import requests
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("API_KEY", "rd_687d733fc4174e70_e1481c3cfb0149a9bfcde7a1cda94db0")
API_URL = "https://api.realitydefender.ai/v1/detect"

def detect_deepfake(video_path: str) -> dict:
    """
    Detect if a video is a deepfake
    
    Args:
        video_path: Path to video file
        
    Returns:
        Detection results as dictionary
    """
    # Validate file exists
    if not os.path.exists(video_path):
        print(f"❌ Error: File not found: {video_path}")
        return {"error": "File not found"}
    
    # Validate file is readable
    if not os.path.isfile(video_path):
        print(f"❌ Error: Not a file: {video_path}")
        return {"error": "Not a file"}
    
    # Get file size
    file_size = os.path.getsize(video_path)
    print(f"📁 File: {video_path}")
    print(f"📊 Size: {file_size / (1024*1024):.2f} MB")
    
    try:
        print("🔄 Uploading video to detection API...")
        
        with open(video_path, "rb") as f:
            files = {"file": f}
            headers = {"x-api-key": API_KEY}
            
            response = requests.post(
                API_URL,
                headers=headers,
                files=files,
                timeout=300
            )
        
        # Check response status
        response.raise_for_status()
        result = response.json()
        
        print("✅ Detection completed successfully!\n")
        print("📋 Results:")
        print(json.dumps(result, indent=2))
        
        # Extract and display key metrics
        if "deepfakeScore" in result:
            score = result["deepfakeScore"]
            percentage = score * 100
            print(f"\n🎯 Deepfake Score: {percentage:.2f}%")
            
            if percentage > 75:
                print("⚠️  LIKELY DEEPFAKE")
            elif percentage > 50:
                print("⚡ POSSIBLY DEEPFAKE")
            elif percentage > 25:
                print("✓ PROBABLY REAL")
            else:
                print("✓✓ LIKELY REAL")
        
        if "requestId" in result:
            print(f"📌 Request ID: {result['requestId']}")
        
        return result
        
    except requests.exceptions.Timeout:
        print("❌ Error: Request timeout. Try a smaller video file.")
        return {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to detection API")
        return {"error": "Connection error"}
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error: API returned {response.status_code}")
        try:
            print(f"   Details: {response.text}")
        except:
            pass
        return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"error": str(e)}

def main():
    """Main entry point"""
    print("=" * 50)
    print("🎬 Deepfake Detection Tool")
    print("=" * 50 + "\n")
    
    # Get video path from command line or use default
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        # Default path - change this to your video location
        video_path = r"C:\Users\yashi\Downloads\video.mp4"
        print(f"⚠️  Using default video path: {video_path}")
        print("   Usage: python detect_fake.py <path_to_video>\n")
    
    # Run detection
    result = detect_deepfake(video_path)
    
    # Return success if no error
    if "error" not in result:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
