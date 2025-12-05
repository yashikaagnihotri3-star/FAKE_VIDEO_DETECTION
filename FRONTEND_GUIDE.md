# 🔗 Frontend Connection Guide

## What You Now Have

✅ **index.html** - Complete frontend with beautiful UI
✅ **server_production.py** - Production backend API
✅ Both ready to work together!

## How to Connect Frontend & Backend

### Step 1: Start the Backend Server
Open Terminal 1:
```powershell
cd c:\Users\yashi\OneDrive\Desktop\deepfake-detector
python run.py
```

Wait for:
```
Started server process
Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open Frontend in Browser
Open any web browser and go to:
```
file:///c:/Users/yashi/OneDrive/Desktop/deepfake-detector/index.html
```

Or open the file directly by double-clicking `index.html`

### That's It! 🎉
Your frontend is now connected to the backend!

---

## How It Works

### Frontend Features
- 📤 **Drag & Drop Upload** - Simply drag videos into the upload area
- 🎥 **Single & Batch** - Upload 1 or multiple videos at once
- 🔍 **Real-time Analysis** - See results instantly
- 📊 **Statistics** - Track deepfakes vs real content
- 🎨 **Beautiful UI** - Modern, responsive design
- 🔄 **Auto-connect** - Auto-detects backend connection
- ✓ **Live Status** - See if backend is connected

### Connection Flow
```
Frontend (index.html)
    ↓
Browser sends video to API
    ↓
Backend (server_production.py)
    ↓
Calls Reality Defender API
    ↓
Returns deepfake score
    ↓
Frontend displays results
```

---

## Using the Frontend

### 1. Upload Videos
- Click upload area or drag files
- Select MP4, MPEG, MOV, or AVI files
- Max 500MB per file

### 2. Analyze
- Click "Analyze Videos" button
- Wait for server to process
- See results appear below

### 3. View Results
- Deepfake Score (0-100%)
- Confidence level
- Verdict (Real or Deepfake)
- Request ID for tracking

---

## API Endpoints Used

The frontend connects to these backend endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Check if backend is online |
| `POST /api/detect` | Upload single video |
| `POST /api/batch-detect` | Upload multiple videos |

---

## Configuration

### Change Backend URL
Edit `index.html` line 381:
```javascript
const API_URL = "http://localhost:8000";
```

Examples:
```javascript
// Local machine
const API_URL = "http://localhost:8000";

// Different port
const API_URL = "http://localhost:8001";

// Remote server
const API_URL = "http://192.168.1.100:8000";

// Production
const API_URL = "https://your-domain.com";
```

---

## Troubleshooting

### "Cannot connect to backend"
1. Make sure backend is running: `python run.py`
2. Backend should show "Running on http://0.0.0.0:8000"
3. Check firewall isn't blocking port 8000

### Videos not uploading
1. Check file format (MP4, MPEG, MOV, AVI)
2. Check file size (max 500MB)
3. Check internet connection
4. See browser console for errors

### Results not showing
1. Wait for backend to process (can take 1-5 minutes)
2. Check browser console (F12) for errors
3. Make sure API_KEY is set in `.env`

---

## Advanced: Host on Web Server

To make it accessible from other devices:

### Option 1: Simple HTTP Server
```powershell
# In project directory
python -m http.server 8001
```

Then access from any device:
```
http://your-computer-ip:8001/index.html
```

### Option 2: Live Server (VS Code)
1. Install "Live Server" extension
2. Right-click `index.html`
3. Click "Open with Live Server"

---

## File Structure

```
deepfake-detector/
├── index.html                 ← FRONTEND (open in browser)
├── server_production.py       ← BACKEND (run with python)
├── run.py                     ← Start script
├── setup.py                   ← Installation
├── requirements_prod.txt      ← Dependencies
├── .env                       ← API Configuration
├── logs/                      ← Server logs
├── results/                   ← Detection results
└── ...other files
```

---

## What Happens When You Upload

1. **Frontend** - You select/drag video
2. **Frontend** - Shows file in list
3. **You Click** - "Analyze Videos"
4. **Frontend** - Sends to http://localhost:8000/api/detect
5. **Backend** - Receives video
6. **Backend** - Calls Reality Defender API
7. **Reality Defender** - Analyzes video (1-5 minutes)
8. **Backend** - Returns deepfake score
9. **Frontend** - Displays results with score & verdict
10. **Backend** - Saves results to JSON file

---

## Ready to Use!

Your complete deepfake detection system is now ready:

✅ Beautiful Frontend
✅ Production Backend
✅ Automatic Connection
✅ Full Video Analysis
✅ Result Tracking

**Start now:**
1. Run backend: `python run.py`
2. Open frontend: Open `index.html` in browser
3. Upload videos and see results!

🚀 Happy analyzing! 🎬
