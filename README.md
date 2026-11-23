# SURAYA AI — Private Personal AI Operating System

Version: 0.4.0

SURAYA AI is a modular personal AI runtime built around the authority chain:

**Creator → Brain → Guardian → Executor → Tools**

The Guardian inspects actions and can block them or require explicit approval. This repository is a private control-plane foundation, not an unrestricted autonomous agent.

## Current capabilities

- FastAPI control plane and health endpoints
- Brain, planner, Guardian policy, approval manager, and executor
- Tool registry with a built-in echo tool
- Local persistent memory, audit log, and secret abstraction
- Local cloud-storage adapter
- Docker deployment foundation and automated tests

Provider integrations, Android console, social publishing, and real-money operations are not considered production-ready merely because their abstractions exist.

## Security boundary

Only `GET /` and `GET /health` are public. Every other API route requires:

```http
Authorization: Bearer <SURAYA_API_TOKEN>
```

Set `SURAYA_API_TOKEN` to a high-entropy random secret in the deployment secret manager. If it is absent, protected routes fail closed with HTTP 503; invalid credentials receive HTTP 401. Never commit the token, put it in a frontend bundle, or send it in a URL.

The secret store encrypts its complete payload at rest using Fernet. Generate `SURAYA_SECRET_KEY` with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Store this key separately in the hosting provider's secret manager. Without it, secret read/write operations fail closed. Losing the key makes the encrypted secret file unrecoverable; back up the key separately from the data disk.

The bearer token currently represents a single trusted operator. Before exposing this control plane to multiple users, add user identities, role-based access, MFA, token rotation/revocation, and an independent security review. Keep the service behind HTTPS and a restrictive network policy. Do not expose it directly to the public internet without those controls.

## Local development

Requirements: Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r backend/requirements.txt
cp env.example .env
# Set SURAYA_API_TOKEN in your local environment before using protected routes.
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Run tests:

```bash
pytest -q
```

## Docker

Build and run:

```bash
docker build -t suraya-ai .
docker run --rm -p 8000:8000 \
  -e SURAYA_API_TOKEN="$SURAYA_API_TOKEN" \
  -v "$(pwd)/data:/app/data" \
  suraya-ai
```

The `data/` directory contains local runtime state and must be backed up. Mount persistent storage in production. The container listens on port 8000.

## Deployment preflight

1. Provision a persistent disk for `/app/data`.
2. Configure `SURAYA_API_TOKEN` and `SURAYA_SECRET_KEY` through the hosting provider's secret manager.
3. Restrict ingress to HTTPS and trusted clients; do not publish the bearer token to browser code.
4. Verify `GET /health` returns HTTP 200.
5. Verify an unauthenticated `GET /status` returns HTTP 503 when the token is missing and HTTP 401 when credentials are invalid.
6. Verify an authenticated `GET /status` and `POST /command` succeed.
7. Confirm audit and memory files survive a container restart.
8. Take and test a backup before enabling any external tools.

## Docker Compose staging

```bash
cp env.example .env
# Set SURAYA_API_TOKEN to a long random token.
# Generate SURAYA_SECRET_KEY with the Fernet command above.
docker compose config --quiet
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1:8000/health
```

The API binds to loopback only. Put a TLS reverse proxy in front of it and keep the bearer token server-side. Compose mounts a named persistent volume at `/app/data`; back up that volume and the Fernet key separately. If the Fernet key is lost, encrypted secrets cannot be recovered.

## Current limitations

- Single shared bearer-token authentication; no end-user accounts or role separation.
- Local state requires persistent storage and tested backups.
- No production-grade multi-instance coordination.
- Tool permissions and approvals are application controls, not a substitute for OS/container sandboxing.
- No unrestricted autonomous financial transactions or custody of customer funds.
