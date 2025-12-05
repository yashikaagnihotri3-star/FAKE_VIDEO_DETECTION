# 🎬 DEEPFAKE DETECTOR - EXACT COMMANDS TO RUN

## Copy & Paste These Commands

### 🔧 ONE TIME SETUP

Open PowerShell and run:

```powershell
cd c:\Users\yashi\OneDrive\Desktop\deepfake-detector
python setup.py
```

Wait for it to complete. You'll see "✅ SETUP COMPLETE!"

---

### 🚀 START THE BACKEND (Every Time)

Open PowerShell and run:

```powershell
cd c:\Users\yashi\OneDrive\Desktop\deepfake-detector
python run.py
```

Keep this terminal window open. Do NOT close it.

Expected output:
```
🚀 STARTING DEEPFAKE DETECTOR BACKEND
...
Uvicorn running on http://0.0.0.0:8000
```

---

### 🌐 OPEN THE FRONTEND (Every Time)

**In Windows Explorer:**
1. Navigate to: `c:\Users\yashi\OneDrive\Desktop\deepfake-detector`
2. Find: `index.html`
3. Double-click it
4. It opens in your default browser

**OR** Copy and paste in address bar:
```
file:///c:/Users/yashi/OneDrive/Desktop/deepfake-detector/index.html
```

---

## ✅ How to Know It's Working

### Backend Running?
- Terminal 1 shows: "Uvicorn running on http://0.0.0.0:8000"
- No errors visible

### Frontend Connected?
- Browser shows: "✓ Connected to backend server"
- Top of page shows status in GREEN

### Test It:
1. Open browser: http://localhost:8000/health
2. You should see:
```json
{
  "status": "healthy",
  "api_connected": true
}
```

---

## 🎯 Complete Workflow

```
START HERE:
    ↓
1. Run: python setup.py
    ↓ (Wait for completion)
2. Open new PowerShell terminal
    ↓
3. Run: python run.py
    ↓ (Keep this running)
4. In Explorer: Open index.html
    ↓
5. You see: ✓ Connected to backend
    ↓
6. Drag videos to upload area
    ↓
7. Click: Analyze Videos
    ↓
8. Wait for results...
    ↓
DONE! See deepfake score ✓
```

---

## 📍 File Locations (Exactly as is)

### Setup Script:
```
c:\Users\yashi\OneDrive\Desktop\deepfake-detector\setup.py
```

### Startup Script:
```
c:\Users\yashi\OneDrive\Desktop\deepfake-detector\run.py
```

### Frontend:
```
c:\Users\yashi\OneDrive\Desktop\deepfake-detector\index.html
```

### Backend:
```
c:\Users\yashi\OneDrive\Desktop\deepfake-detector\server_production.py
```

---

## ⚠️ IF SOMETHING GOES WRONG

### Backend won't start?
```powershell
python setup.py
```
Then try again:
```powershell
python run.py
```

### Can't connect to backend?
1. Check Terminal 1 is still running
2. Check no errors in Terminal 1
3. Refresh browser (F5)
4. Check: http://localhost:8000/health

### Videos won't upload?
1. Check backend is running
2. Check file size < 500MB
3. Check file format (MP4, MPEG, MOV, AVI)
4. Open browser console (F12) for errors

### Port already in use?
```powershell
netstat -ano | findstr :8000
# Find the PID number, then:
taskkill /PID <PID> /F
# Then start again:
python run.py
```

---

## 🔄 Daily Usage (After Setup)

**Every day you want to use it:**

Terminal 1:
```powershell
cd c:\Users\yashi\OneDrive\Desktop\deepfake-detector
python run.py
```

Then open in browser:
```
c:\Users\yashi\OneDrive\Desktop\deepfake-detector\index.html
```

That's it! Upload and analyze videos.

---

## 📊 What Each Script Does

| Script | What it does | When to run |
|--------|-------------|------------|
| `setup.py` | Installs packages, creates folders | Once at beginning |
| `run.py` | Starts the backend server | Every time before use |
| `index.html` | Opens frontend in browser | Every time after run.py |

---

## 🎬 YOU'RE READY!

Just run these 3 commands:
1. `python setup.py` (once)
2. `python run.py` (every time)
3. Open `index.html` (every time)

✓ Backend running
✓ Frontend open
✓ Ready to analyze videos!

Start uploading! 🚀
