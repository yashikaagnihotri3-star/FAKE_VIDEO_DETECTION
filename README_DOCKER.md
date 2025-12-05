Deepfake Detector — Docker & Compose

This README shows how to run your site as a self-hosted website using Docker and Docker Compose.

Files added:
- `Dockerfile` — builds the FastAPI backend image
- `nginx.conf` — serves `index.html` and proxies `/api` to the backend container
- `docker-compose.yml` — orchestrates `web` (nginx) + `backend` services
- `.dockerignore` — reduces build context

Quick local run (Linux/VPS with Docker):

1. Build and start services

```powershell
# From repository root
docker-compose build
docker-compose up -d
```

2. Visit http://localhost

- `nginx` serves `index.html` on port 80.
- `nginx` proxies requests from `/api` to the backend running on port 8000 inside the compose network.

Persistent runtime notes:
- `docker-compose.yml` uses `restart: unless-stopped` so containers restart when the host reboots.
- Ensure your host has Docker and Docker Compose installed.

Deploying to your domain with HTTPS (recommended options):

Option A — Caddy (automatic HTTPS):
- Install Caddy on your VPS and configure it to reverse-proxy to the `web` container or run Caddy in front of the `web` container.
- Caddy automatically obtains TLS certificates from Let's Encrypt.

Option B — Use a provider (Render, Fly, Railway, DigitalOcean App Platform):
- Push this repo to GitHub and create services according to the provider docs.
- They typically provide HTTPS and automatic deploys from Git.

DNS:
- Point your domain's A record to your VPS public IP.
- If you use a load-balancer or reverse proxy, point the domain accordingly.

Security & next steps:
- Switch `DETECTOR_MODE` to `reality` and set `API_KEY` in the environment when ready to use a real detector.
- Add rate-limiting and authentication for production.
- Consider using a managed TLS reverse proxy (Caddy, Traefik) or Let’s Encrypt via Certbot.

If you want, I can:
- Add a `Caddyfile` to this repo so Caddy can run as a container and manage TLS automatically.
- Create GitHub Actions to build and push images to a registry.
- Prepare a short `systemd` unit to ensure `docker-compose` starts on boot (if you run on a VPS).

Which of these would you like me to add next?
