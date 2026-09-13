# Sellince-agent

Turning passive mobile apps into revenue engines. AI sales agent that knows when to reach out and what to offer.

Monorepo with the platform frontend and backend side by side:

- `frontend/` : React 19 + Vite + Tailwind dashboard (auth, onboarding, dashboard)
- `backend/` : FastAPI backend (auth, tenant-fenced chat + AI agent, use-case seed data)

Branches: `integration` (frontend + backend + agent wired), `main` (frontend work),
`kareem/agent-integration` (AI agent work), `manar/rag-final` (RAG catalog work,
mostly merged into integration).

## Run it locally

**Backend - FastAPI on :8000**

```
cd backend
python3 -m pip install -r requirements.txt
cp .env.example .env        # set DATABASE_URL, JWT_SECRET_KEY; GROQ_API_KEY optional
python3 -m alembic upgrade head   # create the schema (Postgres must be running first)
python3 -m app.seed --reset # seeds 20 customers (medium is the default scale)
python3 -m uvicorn app.main:app --port 8000
```

Optional, to enable semantic product search via the RAG vector store:

```
python3 -m scripts.ingest_products
```

Uses Python 3.12 directly (no venv needed; runs against the framework Python where
the deps were installed).

**Frontend - React 19 + Vite on :3000**

```
cd frontend
npm install
cp .env.example .env        # VITE_API_BASE_URL=http://localhost:8000/api/v1
npm run dev
```

Open http://localhost:3000 and log in with the seed account
`ahmad@orange.com` / `Sellince123!` (or sign up fresh).

**Tests**

```
cd backend && python3 -m pytest         # 69 passing, 1 skipped
cd frontend && npm run build            # type/build check
```

## What's wired up (on `integration`)

- Auth: signup/login with JWT + rotating refresh-token cookie; session validated on
  load (`/auth/me`), axios interceptor auto-refreshes on 401.
- Dashboard: tenant-scoped summary computed from real seed data.
- Conversations: tenant inbox + thread detail.
- AI agent: chat with a customer via `POST /api/v1/chat` (Groq, rule-based fallback);
  each exchange is persisted so it shows up in the inbox and dashboard.
- Onboarding company info: company name/industry/plan are real and editable
  (`PATCH /auth/me`). Settings and Analytics are still placeholder screens.

The AI Agent and Conversations screens are temporary demo pages built for integration
testing (you type as the customer to see how the agent replies). They will be replaced
by the real frontend screens when they land.