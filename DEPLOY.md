# Deepfake Detector — Production Deployment with Caddy

Your site is ready to deploy. Caddy handles automatic HTTPS, reverse-proxy, and static file serving.

## Files You Have

- `Dockerfile` — FastAPI backend
- `docker-compose.yml` — Backend + Caddy (reverse-proxy with auto HTTPS)
- `Caddyfile` — Caddy config (edit domain here)
- `index.html` — Frontend
- `server_production.py` — Backend with retry queue & mock mode

## Quick Deployment (5 minutes)

### Step 1: Get a VPS
Pick one (all work great):
- **DigitalOcean** ($5/month) — easiest, good docs
- **Hetzner** ($2.50/month) — cheapest, fast
- **Linode** ($5/month) — reliable
- **AWS Lightsail** ($3.50/month) — AWS ecosystem

**Minimum specs:**
- 1 CPU, 1GB RAM
- Ubuntu 22.04 LTS
- Public IP

### Step 2: Install Docker on VPS

SSH into your VPS and run:

```bash
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
# Log out and back in, or run:
newgrp docker
```

### Step 3: Clone Your Project

```bash
git clone <your-repo-url> deepfake-detector
cd deepfake-detector
```

(Or upload the folder directly via SFTP if not using Git.)

### Step 4: Edit Caddyfile with Your Domain

Edit `Caddyfile` and replace `example.com` with your domain:

```
yourdomain.com {
    # ... rest stays the same
}
```

### Step 5: Point DNS to VPS

In your domain registrar (Namecheap, GoDaddy, etc.):
- Add an **A record**: `yourdomain.com` → your VPS public IP
- Wait 5-30 minutes for DNS to propagate

Test: `nslookup yourdomain.com` should return your VPS IP.

### Step 6: Start the Site

```bash
docker-compose up -d
```

That's it! Visit `https://yourdomain.com` — Caddy automatically:
- Obtains TLS cert from Let's Encrypt
- Serves your frontend
- Proxies `/api/*` to backend
- Handles HTTPS redirects

### Step 7: Verify

```bash
# Check logs
docker-compose logs -f caddy

# Check health
curl https://yourdomain.com/health
```

---

## Configuration Options

### Switch to Real Detector Mode

Edit `docker-compose.yml` and change:

```yaml
environment:
  - DETECTOR_MODE=reality
  - API_KEY=your_api_key_here
  - DETECTOR_API_URL=https://api.realitydefender.ai/v1/detect
```

Then restart:

```bash
docker-compose restart backend
```

### Increase File Upload Limit

Edit `Caddyfile` and add (before the closing brace):

```
request_header -l Content-Length 0 1073741824  # 1GB max
```

### View Logs

```bash
# Caddy logs
docker-compose logs -f caddy

# Backend logs
docker-compose logs -f backend

# All logs
docker-compose logs -f
```

### Stop the Site

```bash
docker-compose down
```

### Restart (e.g., after config changes)

```bash
docker-compose restart
```

---

## Persistent Data

Your uploads, results, and queue are stored in local volumes:
- `./uploads/` — video files
- `./results/` — detection results
- `./queue/` — retry queue for failed requests
- `caddy-data/` — Let's Encrypt certs (backed up by Caddy)

These survive container restarts and updates.

---

## Updating Your Site

1. Make changes locally
2. Commit and push to GitHub
3. SSH into VPS
4. Pull changes: `git pull`
5. Rebuild and restart: `docker-compose up -d --build`

---

## Troubleshooting

**Site not loading:**
```bash
docker-compose logs caddy
```
Check if DNS has propagated: `nslookup yourdomain.com`

**Backend errors:**
```bash
docker-compose logs backend
```

**Caddy can't get TLS cert:**
- Verify DNS is pointing to VPS: `dig yourdomain.com`
- Port 80 must be open (Caddy uses ACME-01 challenge)
- Wait 5-10 min for DNS to propagate

**Out of disk space:**
```bash
docker system prune -a
```

---

## Next Steps (Optional)

- Add rate-limiting to `Caddyfile`
- Set up monitoring with `docker stats`
- Backup `caddy-data/` volume regularly
- Use GitHub Actions to auto-deploy on push

You're live! 🎬
