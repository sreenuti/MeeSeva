# India AI Citizen Services Platform

Secure, AI-assisted citizen application preparation platform (initial geography: Andhra Pradesh).

> Working repository name may differ from the eventual commercial brand. Avoid implying government affiliation.

## Milestone status

- **M0** — Product alignment & architecture (docs/)
- **M1** — Secure identity & document vault (**implemented**)
- **M2** — Document intelligence & verified profile (**implemented**, pending review)
- M3+ — Not started

## Quick start (development auth)

```bash
# 1) Start Postgres + API (+ optional web)
docker compose up --build

# 2) Or run API locally
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
set ENVIRONMENT=development
set AUTH_MODE=dev
set AUTH_DEV_MODE=true
set DATABASE_URL=postgresql+psycopg://citizen:citizen@localhost:5432/citizen_services
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 3) Web
cd apps/web
npm install
set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
set NEXT_PUBLIC_AUTH_MODE=dev
npm run dev
```

Open http://localhost:3000 — use distinct dev subjects to verify isolation.

## Cognito

See [docs/M1_COGNITO_SETUP.md](docs/M1_COGNITO_SETUP.md). Dev auth is refused when `ENVIRONMENT` is `staging` or `production`.

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

```bash
cd apps/web
npm install
npm run typecheck
npm run build
```

## Security notes

- Ownership is always derived from the verified JWT subject → local user mapping.
- Uploads are content-validated; malware scan is fail-closed before download.
- Synthetic documents only until compliance approval.
