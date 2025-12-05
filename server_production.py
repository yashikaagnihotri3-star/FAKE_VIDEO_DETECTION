#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production-ready Deepfake Detector Backend
With retry queue, proxy support, mock mode, and background worker
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import json
from pathlib import Path
import aiofiles
import asyncio
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import sys

# Force UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
	import io
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
	sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create directories
Path("logs").mkdir(exist_ok=True)
Path("uploads").mkdir(exist_ok=True)
Path("results").mkdir(exist_ok=True)
Path("queue").mkdir(exist_ok=True)

# Configuration
DETECTOR_API_URL = os.getenv("DETECTOR_API_URL", "https://api.realitydefender.ai/v1/detect")
API_KEY = os.getenv("API_KEY")
DETECTOR_MODE = os.getenv("DETECTOR_MODE", "reality").lower()  # 'reality' or 'mock'
HTTP_PROXY = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
HTTPS_PROXY = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

if not API_KEY and DETECTOR_MODE != 'mock':
	logger.error("CRITICAL: API_KEY not set in environment variables (required for 'reality' mode)")
else:
	logger.info("✓ API_KEY loaded successfully or mock mode active")

if DETECTOR_MODE == "mock":
	logger.info("⚠️ Running in MOCK detector mode — no external API calls will be made")


# Helper: HTTP session with retries and proxy support
def setup_http_session():
	"""Create a requests.Session with retry strategy and optional proxies."""
	session = requests.Session()
	retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["POST", "GET", "OPTIONS"])
	adapter = HTTPAdapter(max_retries=retries)
	session.mount('https://', adapter)
	session.mount('http://', adapter)

	proxies = {}
	if HTTPS_PROXY:
		proxies['https'] = HTTPS_PROXY
	if HTTP_PROXY:
		proxies['http'] = HTTP_PROXY
	if proxies:
		session.proxies.update(proxies)
		logger.info(f"Using proxies: {proxies}")

	return session


# Send to detector (blocking; safe to call in threadpool)
def send_to_detector(session, video_bytes, filename, content_type, request_id):
	"""Sends data to the external detector. Returns dict on success, None if queued."""
	# Mock mode: generate deterministic pseudo-result
	if DETECTOR_MODE == 'mock':
		score = round(random.uniform(0, 1), 3)
		mock_result = {
			"deepfakeScore": score,
			"confidence": round(random.uniform(0.5, 0.99), 2),
			"notes": "mocked result"
		}
		logger.info(f"[{request_id}] Mock detector returned score={score}")
		return mock_result

	if not session:
		session = setup_http_session()

	try:
		resp = session.post(
			DETECTOR_API_URL,
			headers={"x-api-key": API_KEY},
			files={"file": (filename, video_bytes, content_type)},
			timeout=120
		)
		resp.raise_for_status()
		return resp.json()
	except requests.exceptions.RequestException as e:
		# Connection issue — persist to queue for retry
		logger.error(f"[{request_id}] send_to_detector failed: {str(e)} — enqueueing for retry")
		try:
			# Save bytes to uploads and metadata to queue
			safe_name = filename.replace('/', '_').replace('\\', '_')
			upload_path = Path(f"uploads/{request_id}__{safe_name}")
			with open(upload_path, 'wb') as f:
				f.write(video_bytes)
			meta = {
				"request_id": request_id,
				"filename": filename,
				"content_type": content_type,
				"upload_path": str(upload_path),
				"timestamp": datetime.now().isoformat()
			}
			queue_file = Path(f"queue/{request_id}.json")
			with open(queue_file, 'w') as f:
				json.dump(meta, f)
			logger.info(f"[{request_id}] Saved to queue for later retry")
		except Exception as ex:
			logger.error(f"Failed to write to queue: {str(ex)}")
		return None


# Background retry worker (async)
async def retry_worker(app: FastAPI):
	"""Background worker that retries queued requests."""
	logger.info("Retry worker started")
	session = getattr(app.state, 'http_session', None) or setup_http_session()
	try:
		while True:
			queue_dir = Path('queue')
			for qfile in queue_dir.glob('*.json'):
				try:
					with open(qfile, 'r') as f:
						meta = json.load(f)
					request_id = meta.get('request_id')
					upload_path = meta.get('upload_path')
					if not upload_path or not Path(upload_path).exists():
						logger.warning(f"Queue item {qfile} missing upload file; removing")
						qfile.unlink(missing_ok=True)
						continue
					with open(upload_path, 'rb') as f:
						video_bytes = f.read()

					logger.info(f"[RETRY-{request_id}] Attempting retry")
					# run blocking send in thread pool
					result = await asyncio.to_thread(send_to_detector, session, video_bytes, meta.get('filename'), meta.get('content_type'), request_id)
					if result is not None:
						# store result and cleanup
						detection_results[request_id] = {
							"request_id": request_id,
							"status": "success",
							"filename": meta.get('filename'),
							"timestamp": datetime.now().isoformat(),
							"detection_result": result,
							"deepfake_score": result.get('deepfakeScore', 0),
							"is_deepfake": result.get('deepfakeScore', 0) > 0.5
						}
						await save_result(request_id, detection_results[request_id])
						# remove queue and upload files
						Path(upload_path).unlink(missing_ok=True)
						qfile.unlink(missing_ok=True)
						logger.info(f"[RETRY-{request_id}] Retry successful and cleaned up")
					else:
						logger.info(f"[RETRY-{request_id}] Still failed; will retry later")
				except Exception as e:
					logger.error(f"Error processing queue file {qfile}: {str(e)}")
			await asyncio.sleep(10)
	except asyncio.CancelledError:
		logger.info("Retry worker cancelled")
	except Exception as e:
		logger.error(f"Retry worker crashed: {str(e)}")


# FastAPI app and lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("🚀 Deepfake Detector Backend Starting...")
	logger.info(f"   API URL: {DETECTOR_API_URL}")
	logger.info(f"   Max File Size: {MAX_FILE_SIZE / (1024*1024):.0f}MB")
	# Prepare HTTP session with retries and optional proxy
	app.state.http_session = setup_http_session()
	# Start background retry worker
	app.state.retry_task = asyncio.create_task(retry_worker(app))
	yield
	# Shutdown
	if hasattr(app.state, "retry_task"):
		app.state.retry_task.cancel()
		try:
			asyncio.get_event_loop().run_until_complete(app.state.retry_task)
		except Exception:
			pass
	logger.info("🛑 Deepfake Detector Backend Shutting Down...")


# Initialize app
app = FastAPI(title="Deepfake Detector", version="2.0", lifespan=lifespan)

# CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

# In-memory results storage
detection_results = {}


# Helper: Save result to file
async def save_result(request_id: str, result: dict):
	"""Save detection result to results/ directory."""
	results_dir = Path("results")
	results_dir.mkdir(exist_ok=True)
	result_file = results_dir / f"{request_id}.json"
	async with aiofiles.open(result_file, 'w') as f:
		await f.write(json.dumps(result, indent=2))
	logger.info(f"[{request_id}] Result saved to {result_file}")


# Routes
@app.get("/")
async def home():
	"""Serve the frontend HTML."""
	with open("index.html", "r", encoding="utf-8") as f:
		return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
	"""Health check endpoint with detector mode and API connectivity."""
	api_connected = False
	if DETECTOR_MODE != 'mock':
		try:
			session = getattr(app.state, 'http_session', None) or setup_http_session()
			# Non-blocking OPTIONS check
			resp = session.options(DETECTOR_API_URL, timeout=5)
			api_connected = resp.status_code < 400
		except Exception:
			api_connected = False
	else:
		api_connected = True  # Mock mode doesn't need external API

	return JSONResponse({
		"status": "ok",
		"detector_mode": DETECTOR_MODE,
		"api_connected": api_connected,
		"timestamp": datetime.now().isoformat()
	})


@app.post("/api/detect")
async def detect(video_file: UploadFile = File(...)):
	"""Detect deepfake in a single video."""
	request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
	logger.info(f"[{request_id}] New detection request: {video_file.filename}")

	try:
		content = await video_file.read()
		if len(content) > MAX_FILE_SIZE:
			logger.error(f"[{request_id}] File too large: {len(content)} > {MAX_FILE_SIZE}")
			raise HTTPException(status_code=413, detail="File too large")

		# Call detector in thread pool
		session = getattr(app.state, 'http_session', None) or setup_http_session()
		result = await asyncio.to_thread(send_to_detector, session, content, video_file.filename, video_file.content_type or "video/mp4", request_id)

		if result is not None:
			# Success
			response_obj = {
				"request_id": request_id,
				"status": "success",
				"filename": video_file.filename,
				"timestamp": datetime.now().isoformat(),
				"detection_result": result,
				"deepfake_score": result.get('deepfakeScore', 0),
				"confidence": result.get('confidence', 0),
				"is_deepfake": result.get('deepfakeScore', 0) > 0.5
			}
			detection_results[request_id] = response_obj
			await save_result(request_id, response_obj)
			return JSONResponse(status_code=200, content=response_obj)
		else:
			# Queued
			response_obj = {
				"request_id": request_id,
				"status": "queued",
				"filename": video_file.filename,
				"timestamp": datetime.now().isoformat(),
				"message": "Detection request queued for retry"
			}
			detection_results[request_id] = response_obj
			return JSONResponse(status_code=202, content=response_obj)

	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"[{request_id}] Error: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch-detect")
async def batch_detect(files: list[UploadFile] = File(...)):
	"""Detect deepfakes in multiple videos."""
	batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
	logger.info(f"[{batch_id}] Batch detection: {len(files)} files")

	results_list = []
	session = getattr(app.state, 'http_session', None) or setup_http_session()

	for file in files:
		request_id = f"{batch_id}__{file.filename.replace('.', '_')}"
		try:
			content = await file.read()
			if len(content) > MAX_FILE_SIZE:
				results_list.append({
					"request_id": request_id,
					"status": "error",
					"filename": file.filename,
					"error": "File too large"
				})
				continue

			result = await asyncio.to_thread(send_to_detector, session, content, file.filename, file.content_type or "video/mp4", request_id)
			if result is not None:
				response_obj = {
					"request_id": request_id,
					"status": "success",
					"filename": file.filename,
					"timestamp": datetime.now().isoformat(),
					"detection_result": result,
					"deepfake_score": result.get('deepfakeScore', 0),
					"confidence": result.get('confidence', 0),
					"is_deepfake": result.get('deepfakeScore', 0) > 0.5
				}
				detection_results[request_id] = response_obj
				await save_result(request_id, response_obj)
				results_list.append(response_obj)
			else:
				response_obj = {
					"request_id": request_id,
					"status": "queued",
					"filename": file.filename,
					"timestamp": datetime.now().isoformat()
				}
				detection_results[request_id] = response_obj
				results_list.append(response_obj)
		except Exception as e:
			logger.error(f"[{request_id}] Error: {str(e)}")
			results_list.append({
				"request_id": request_id,
				"status": "error",
				"filename": file.filename,
				"error": str(e)
			})

	return JSONResponse(status_code=200, content={
		"batch_id": batch_id,
		"timestamp": datetime.now().isoformat(),
		"results": results_list
	})


@app.get("/api/results/{request_id}")
async def get_result(request_id: str):
	"""Retrieve detection result by request ID."""
	if request_id in detection_results:
		return JSONResponse(status_code=200, content=detection_results[request_id])

	results_file = Path("results") / f"{request_id}.json"
	if results_file.exists():
		async with aiofiles.open(results_file, 'r') as f:
			content = await f.read()
			return JSONResponse(status_code=200, content=json.loads(content))

	raise HTTPException(status_code=404, detail="Result not found")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
	logger.error(f"Unhandled exception: {str(exc)}")
	return JSONResponse(status_code=500, content={"detail": str(exc)})


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(
		"server_production:app",
		host="0.0.0.0",
		port=8000,
		reload=False,
		log_level="info"
	)
