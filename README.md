# 🎬 Deepfake Detector

A production-ready deepfake detection website built with FastAPI, Docker, and Caddy.

## Features

✅ **Beautiful UI** - Purple gradient interface for video upload
✅ **Real-time Detection** - Instant deepfake analysis with confidence scores
✅ **Statistics Dashboard** - Live tracking of analyzed videos
✅ **Auto Retry Queue** - Handles API failures gracefully
✅ **Docker Ready** - Deploy anywhere with Docker Compose
✅ **Auto HTTPS** - Caddy manages Let's Encrypt certificates
✅ **Mock Mode** - Test without external API
✅ **Persistent Storage** - Uploads, results, and queue survive restarts

## Quick Start (Local)

### Prerequisites
- Docker & Docker Compose installed

### Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/deepfake-detector.git
cd deepfake-detector

# Start services (builds Docker images)
docker-compose up -d

# Visit http://localhost
```

## Deploy to Your Domain (5 minutes)

See `DEPLOY.md` for complete instructions.

**Quick steps:**
1. Get a VPS (DigitalOcean, Hetzner, Linode, etc.)
2. Install Docker
3. Clone this repo
4. Edit `Caddyfile` → replace `example.com` with your domain
5. Point DNS A record to VPS IP
6. Run `docker-compose up -d`
7. Wait 5 min for Caddy to auto-obtain HTTPS cert
8. Visit `https://yourdomain.com` ✅

## File Structure

```
deepfake-detector/
├── server_production.py    # FastAPI backend with retry queue
├── index.html              # Beautiful responsive frontend
├── Dockerfile              # Backend container image
├── docker-compose.yml      # Orchestrates Caddy + backend
├── Caddyfile               # Auto HTTPS reverse proxy config
├── nginx.conf              # (alternative) nginx config
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build config
├── DEPLOY.md              # Full deployment guide
├── deploy.sh              # Auto-deployment script
├── deepfake-detector.service  # systemd auto-start (optional)
└── README.md              # This file
```

## Features

- **Upload UI** — Drag & drop video files, single or batch
- **Real-time Analysis** — Instant deepfake scoring (0-100%)
- **Live Stats** — Dashboard shows Total Analyzed, Deepfakes Found, Real Content
- **Auto Retry** — Failed requests automatically retry every 10 seconds
- **Mock Mode** — Test without external API (default)
- **Reality Mode** — Connect to Reality Defender AI API
- **Persistent** — Uploads, results, queue survive restarts
- **Auto HTTPS** — Caddy manages free Let's Encrypt certs
- **Docker Ready** — One command: `docker-compose up -d`

## Configuration

### Enable Real Deepfake Detection

Edit `docker-compose.yml`:

```yaml
backend:
  environment:
    - DETECTOR_MODE=reality
    - API_KEY=your_reality_defender_api_key
    - DETECTOR_API_URL=https://api.realitydefender.ai/v1/detect
```

Get API key: https://www.realitydefender.ai/

### Change Domain

Edit `Caddyfile`:
```
yourdomain.com {
    # Caddy auto-manages HTTPS for this domain
    ...
}
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Serve frontend HTML |
| GET | `/health` | Health check (detector mode + API status) |
| POST | `/api/detect` | Single video detection |
| POST | `/api/batch-detect` | Multiple videos at once |
| GET | `/api/results/{id}` | Retrieve result by request ID |

## Troubleshooting

**Site not loading?**
```bash
docker-compose logs caddy
```

**Backend errors?**
```bash
docker-compose logs backend
```

**Need to rebuild?**
```bash
docker-compose down
docker-compose up -d --build
```

**View live logs:**
```bash
docker-compose logs -f
```

## License

MIT — Use freely!

## Support

- 📖 Full guide: `DEPLOY.md`
- 🐳 Docker docs: https://docs.docker.com/
- 🔐 Caddy docs: https://caddyserver.com/docs/
For code issues: Check the error messages and ensure all dependencies are installed.
