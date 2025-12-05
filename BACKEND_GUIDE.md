# 🎬 Perfect Backend Setup

## Installation (One time)

### 1. Run Setup Script
```powershell
python setup.py
```

This will:
- ✓ Check Python version
- ✓ Create directories (logs, uploads, results)
- ✓ Install all dependencies
- ✓ Verify configuration
- ✓ Run health checks

### 2. Verify API Key
Make sure `.env` file has your API key:
```
API_KEY=rd_687d733fc4174e70_e1481c3cfb0149a9bfcde7a1cda94db0
```

## Running the Backend

### Option 1: Simple Start (Recommended)
```powershell
python run.py
```

### Option 2: Direct with Uvicorn
```powershell
uvicorn server_production:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Production Mode (No Reload)
```powershell
uvicorn server_production:app --host 0.0.0.0 --port 8000
```

## Access the Backend

Once running, open your browser:

- **🏠 Home**: http://localhost:8000
- **📖 API Docs**: http://localhost:8000/docs
- **🏥 Health**: http://localhost:8000/health

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with UI |
| GET | `/health` | Health check |
| POST | `/api/detect` | Upload single video |
| POST | `/api/batch-detect` | Upload multiple videos |
| GET | `/api/results/{id}` | Get detection results |
| GET | `/docs` | Interactive API docs |

## Upload a Video

### Using cURL
```powershell
curl -X POST "http://localhost:8000/api/detect" `
  -F "video_file=@C:\path\to\video.mp4"
```

### Using Python
```python
import requests

with open("video.mp4", "rb") as f:
    files = {"video_file": f}
    response = requests.post(
        "http://localhost:8000/api/detect",
        files=files
    )
    print(response.json())
```

## Example Response

```json
{
  "request_id": "20231205120000_video.mp4",
  "status": "success",
  "filename": "video.mp4",
  "file_size_mb": 15.32,
  "timestamp": "2023-12-05T12:00:00",
  "deepfake_score": 0.23,
  "is_deepfake": false,
  "confidence": 0.95,
  "detection_result": {
    "deepfakeScore": 0.23,
    "confidence": 0.95,
    "requestId": "req_123456"
  }
}
```

## Features

✅ **Production Ready** - Async, error handling, logging
✅ **Batch Processing** - Upload multiple videos at once
✅ **Result Storage** - Results saved to JSON files
✅ **Background Tasks** - File saving in background
✅ **CORS Enabled** - Frontend integration ready
✅ **Detailed Logging** - Monitor every request
✅ **Health Check** - Verify service status
✅ **Interactive UI** - Beautiful web interface
✅ **API Documentation** - Swagger UI with examples

## Project Structure

```
deepfake-detector/
├── server_production.py      # Main production server
├── run.py                    # Start script
├── setup.py                  # Installation script
├── requirements_prod.txt     # Dependencies
├── .env                      # API configuration
├── logs/                     # Server logs
├── results/                  # Detection results
└── uploads/                  # Uploaded files
```

## Troubleshooting

### Port 8000 Already in Use
```powershell
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port:
uvicorn server_production:app --port 8001
```

### Import Errors
```powershell
pip install -r requirements_prod.txt
```

### API Key Issues
- Check `.env` file exists
- Verify API_KEY is set correctly
- Restart server after changing `.env`

## Monitoring

Check logs while server is running:
```powershell
Get-Content logs\* -Tail 20
```

## Performance Tips

1. **File Size**: Keep videos under 500MB
2. **Timeout**: Default 300 seconds (5 min)
3. **Concurrent Uploads**: Server handles multiple simultaneous uploads
4. **Batch Processing**: Use batch endpoint for multiple files

## Support

For issues:
1. Check the logs in `logs/` directory
2. Verify `.env` configuration
3. Check internet connection
4. Ensure API key is valid
5. Review error messages in response

---

🚀 Your perfect backend is ready to go!
