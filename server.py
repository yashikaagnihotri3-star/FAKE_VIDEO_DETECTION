from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Deepfake Detector", version="1.0.0")

# Allow all domains for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DETECTOR_API_URL = "https://api.realitydefender.ai/v1/detect"
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    logger.warning("WARNING: API_KEY not set in environment variables")

@app.get("/", response_class=HTMLResponse)
def home():
    """Home endpoint with usage instructions"""
    return """
    <html>
        <head><title>Deepfake Detector</title></head>
        <body style="font-family: Arial;">
            <h1>🎬 Deepfake Detector Backend</h1>
            <p><strong>Status:</strong> Running ✓</p>
            <h2>API Endpoints:</h2>
            <ul>
                <li><strong>POST /api/detect</strong> - Upload a video to detect if it's a deepfake</li>
                <li><strong>GET /health</strong> - Health check</li>
                <li><strong>POST /api/batch-detect</strong> - Detect multiple videos</li>
            </ul>
            <h2>Usage:</h2>
            <pre>
curl -X POST "http://localhost:8000/api/detect" \\
  -H "Content-Type: multipart/form-data" \\
  -F "video_file=@your_video.mp4"
            </pre>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api_connected": bool(API_KEY)}

@app.post("/api/detect")
async def detect(video_file: UploadFile = File(...)):
    """
    Detect if uploaded video is a deepfake
    
    Args:
        video_file: Video file to analyze
        
    Returns:
        Detection results including confidence scores
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY not configured. Set API_KEY in .env file"
        )
    
    if not video_file:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    # Validate file type
    allowed_types = ["video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo"]
    if video_file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    try:
        logger.info(f"Processing video: {video_file.filename}")
        
        video_bytes = await video_file.read()
        
        # Call Reality Defender API
        response = requests.post(
            DETECTOR_API_URL,
            headers={"x-api-key": API_KEY},
            files={"file": (video_file.filename, video_bytes, video_file.content_type)},
            timeout=300  # 5 minutes for large videos
        )
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"Detection completed for {video_file.filename}")
        
        return {
            "status": "success",
            "filename": video_file.filename,
            "detection_result": result,
            "confidence": result.get("confidence", "N/A"),
            "is_deepfake": result.get("deepfakeScore", 0) > 0.5
        }
        
    except requests.exceptions.Timeout:
        logger.error("API request timeout")
        raise HTTPException(status_code=504, detail="Detection API timeout. Try a smaller video.")
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to detection API")
        raise HTTPException(status_code=503, detail="Detection service unavailable")
    except requests.exceptions.RequestException as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Detection failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/api/batch-detect")
async def batch_detect(files: list[UploadFile] = File(...)):
    """
    Detect multiple videos at once
    
    Args:
        files: Multiple video files to analyze
        
    Returns:
        List of detection results for each file
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY not configured"
        )
    
    results = []
    for video_file in files:
        try:
            video_bytes = await video_file.read()
            response = requests.post(
                DETECTOR_API_URL,
                headers={"x-api-key": API_KEY},
                files={"file": (video_file.filename, video_bytes, video_file.content_type)},
                timeout=300
            )
            response.raise_for_status()
            result = response.json()
            
            results.append({
                "filename": video_file.filename,
                "status": "success",
                "detection_result": result,
                "is_deepfake": result.get("deepfakeScore", 0) > 0.5
            })
        except Exception as e:
            results.append({
                "filename": video_file.filename,
                "status": "error",
                "error": str(e)
            })
    
    return {"status": "completed", "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
