# 📋 COMPLETE STARTUP GUIDE - Run This Step by Step

## 🎯 What You Need to Do

Follow these steps in order. Copy and paste the commands exactly.

---

## ⚙️ STEP 1: Setup (First Time Only)

**Open PowerShell and run this:**

```powershell
cd c:\Users\yashi\OneDrive\Desktop\deepfake-detector
python setup.py
```

**What it does:**
- ✓ Checks Python version
- ✓ Creates folders (logs, uploads, results)
- ✓ Installs all packages
- ✓ Verifies everything works

**Expected output:**
```
✅ SETUP COMPLETE!
Next steps:
1. Run the server: python server_production.py
2. Open browser: http://localhost:8000
```

---

## 🚀 STEP 2: Start the Backend Server

**Open PowerShell Terminal 1 and run:**

```powershell
cd c:\Users\yashi\OneDrive\Desktop\deepfake-detector
python run.py
```

**Keep this running! You should see:**
```
========================================================
🚀 STARTING DEEPFAKE DETECTOR BACKEND
========================================================
Starting at: 2025-12-05 10:30:00

📍 Server Configuration:
   Host: 0.0.0.0
   Port: 8000
   Reload: Enabled

🌐 Access Points:
   Home:    http://localhost:8000
   API Doc: http://localhost:8000/docs
   Health:  http://localhost:8000/health

INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal open!** ← Important

---

## 🌐 STEP 3: Open the Frontend

**Open Windows Explorer and navigate to:**
```
c:\Users\yashi\OneDrive\Desktop\deepfake-detector\index.html
```

**Double-click the file** or right-click → Open with → Your Browser

**You should see:**
- 🎬 Deepfake Detector title
- ✓ Connected to backend server message
- 📤 Upload area ready for videos
- 📊 Statistics section

---

## ✅ STEP 4: Start Using It!

### Upload a Video:
1. Click the upload area (or drag a video)
2. Select a video file (MP4, MPEG, MOV, or AVI)
3. Click "Analyze Videos"
4. Wait for results...

### See the Results:
- **Score**: 0-100% (higher = more likely deepfake)
- **Verdict**: Real or Deepfake indicator
- **Confidence**: How sure the AI is

## Usage

### Option A: Start the Web API Server
```powershell
python server.py
```

Then open your browser:
- **Home**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Option B: Run Standalone Detection Script
```powershell
# Use default video path
python detect_fake.py

# Or specify your video file
python detect_fake.py "C:\path\to\your\video.mp4"
```

### Option C: Test API with cURL
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Upload video for detection
curl -X POST "http://localhost:8000/api/detect" `
  -F "video_file=@C:\path\to\video.mp4"
```

## Files Explanation

| File | Purpose |
|------|---------|
| `server.py` | FastAPI web server with detection endpoints |
| `detect_fake.py` | Standalone CLI tool for quick testing |
| `requirements.txt` | Python package dependencies |
| `.env` | API key configuration (keep private!) |
| `README.md` | Full documentation |
| `test_api.py` | Test suite for API endpoints |

## Expected Output Example

When running `detect_fake.py`:
```
==================================================
🎬 Deepfake Detection Tool
==================================================

📁 File: C:\Users\yashi\Downloads\video.mp4
📊 Size: 15.32 MB
🔄 Uploading video to detection API...
✅ Detection completed successfully!

📋 Results:
{
  "deepfakeScore": 0.23,
  "confidence": 0.95,
  "requestId": "req_abc123"
}

🎯 Deepfake Score: 23.00%
✓✓ LIKELY REAL
📌 Request ID: req_abc123
```

## Interpretation

| Score Range | Meaning |
|-------------|---------|
| 0-25% | ✓✓ Likely Real |
| 25-50% | ✓ Probably Real |
| 50-75% | ⚡ Possibly Deepfake |
| 75-100% | ⚠️ Likely Deepfake |

## Troubleshooting

### "File not found"
- Use absolute file path
- On Windows, use forward slashes or raw strings: `r"C:\path\file.mp4"`

### "API_KEY not configured"
- Ensure `.env` file exists
- Check API_KEY is set correctly
- Restart server after changing `.env`

### "Connection timeout"
- Check internet connection
- Try smaller video files (< 100MB)
- Increase timeout value in code

### "Module not found"
- Run `pip install -r requirements.txt`
- Verify packages are installed: `pip list`

## Next Steps

1. ✅ Install dependencies
2. ✅ Test with `python detect_fake.py`
3. ✅ Start server with `python server.py`
4. ✅ Access API at http://localhost:8000
5. ✅ Upload videos for detection

Happy detecting! 🎬✨
