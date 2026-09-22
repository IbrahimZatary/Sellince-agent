# Sellince-agent

Turning passive mobile apps into revenue engines. AI sales agent that knows when to reach out and what to offer.

Monorepo, three apps side by side:

- `backend/` — FastAPI API on **:8000** (auth, chat + AI agent, dashboard, conversations, attributions)
- `frontend/admin/` — React 19 + Vite dashboard on **:5174** (login, dashboard, conversations inbox)
- `frontend/customer/` — React 19 + Vite customer app on **:5173** (home, login, chat, checkout)

## Prerequisites

- Python 3.12
- Node 20+
- PostgreSQL 14+ running locally
- Groq API key (optional — without it the agent falls back to rule-based replies)

## Run it from scratch

### 1. Backend — FastAPI on :8000

```
cd backend
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Fill in `backend/.env`:

```
DATABASE_URL=postgresql://postgres:devpass@localhost:5432/sellince
JWT_SECRET_KEY=<output of: openssl rand -hex 32>
GROQ_API_KEY=<optional, enables the LLM paths>
```

`DATABASE_URL` assumes user `postgres` / password `devpass` (same as the
test suite), change it to match your local Postgres if yours differ

Then create the database, migrate, and seed the exact demo snapshot:

```
createdb sellince
python3 -m alembic upgrade head
python3 -m app.seed --reset
python3 -m uvicorn app.main:app --port 8000
```

Optional, to enable semantic product search via the RAG vector store
(`backend/chroma_db/`, gitignored — rebuilt by this script):

```
python3 -m scripts.ingest_products
```

Health check: `curl http://localhost:8000/health` → `{"status":"ok"}`.

### 2. Admin dashboard — :5174

```
cd frontend/admin
npm install
cp .env.example .env   # optional; default API base is http://localhost:8000/api/v1
npm run dev
```

Open http://localhost:5174 and log in:

| Email | Password | Company | Role |
|---|---|---|---|
| `ahmad@orange.com` | `Sellince123!` | Orange | admin |
| `rania@orange.com` | `Sellince123!` | Orange | agent |
| `omar@zain.com` | `Sellince123!` | Zain | admin |
| `fatima@zain.com` | `Sellince123!` | Zain | agent |

### 3. Customer app — :5173

```
cd frontend/customer
npm install
cp .env.example .env   # optional; default API base is http://localhost:8000
npm run dev
```

Open http://localhost:5173 and log in with a customer **phone number** + `Sellince123!`.
Seeded customers with live triggers (Orange):

| Phone | Customer | Why the agent reaches out |
|---|---|---|
| `0781111111` | Ahmed Al-Fayez | 92% data usage → upgrade offer |
| `0782222222` | Layla Hassan | contract expiring → renewal offer |
| `0785555555` | Sara Ali | 95% data usage → upgrade offer |
| `0780222222` | Amal Dajah | 90% fiber usage → broadband offer |
| `0794567890` | Tamer Saliba (Zain) | prepaid heavy user → postpaid offer |

Tip: you can also open the chat directly as a customer, e.g.
`http://localhost:5173/chat?customer_id=4`.

## The demo flow

1. Customer says hi in the customer app → the agent replies with a real offer
   (`POST /api/v1/chat`).
2. Customer accepts ("I want it") → the agent returns a **Continue to Purchase**
   button with a `/checkout?...&attribution_id=...` URL.
3. Fill the (demo) payment form and pay → `POST /api/v1/attributions/checkout/complete`
   marks the attribution `completed`, updates the customer's plan, and resets usage.
4. Watch it land in the admin app: dashboard revenue trend + revenue-by-offer,
   conversations inbox, and recent activity.

Attribution lifecycle: `pending` (checkout shown) → `completed` (paid) | `expired`
(abandoned). Dashboards count `completed` as revenue.

## Tests

```
cd backend && python3 -m pytest            # 63 passing, 1 skipped (needs local Postgres; creates sellince_test automatically)
cd ../frontend/admin && npm run build      # vite build
cd ../frontend/admin && npm run lint       # oxlint (warnings only)
cd ../frontend/customer && npm run check   # eslint + prettier + vitest (24 tests) + build
```

## Seed data

`python3 -m app.seed --reset` restores the exact snapshot every clone starts from:
2 companies, 4 users, 20 customers, 13 conversations, 42 messages, 8 offers,
6 attributions. Plain `python3 -m app.seed` upserts to the same state without
truncating. (`--scale` is accepted for backwards compatibility but ignored.)

## Troubleshooting

- `connection refused` on `:5432` → Postgres isn't running; start it first.
- `alembic upgrade head` fails → check `DATABASE_URL` in `backend/.env`.
- Agent replies are generic/template-only → set `GROQ_API_KEY` in `backend/.env`
  (rule-based fallback is intentional without it).
- `EADDRINUSE` on `:8000` / `:5173` / `:5174` → a previous dev server is still
  running; stop it and retry.
- RAG search returns nothing → run `python3 -m scripts.ingest_products` from
  `backend/` to rebuild `chroma_db/`.
