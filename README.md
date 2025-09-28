# sprint-marketing-bot
AI Agent for Sprint that is going to be a foundational basis for further modules

## Docker stack

- One-liner: `./scripts/docker-up.ssh` builds images, starts the stack, and runs ingest if the FAISS index is missing (pass `--dev` to mount source code into the containers for instant reloads).
- Build everything manually with `docker compose build` and start the stack using `docker compose up -d` if you want to control each step.
- The reverse proxy (Caddy) exposes the UI on `http://localhost` (also available via TLS on `https://localhost` with Caddy's internal cert) and forwards `/api/*` requests to the FastAPI service.
- Health probes: `GET /health` (liveness) and `GET /ready` (readiness) tunnelled through the proxy at `/api/health` and `/api/ready`.
- Data persistence uses named volumes mapped to `/data/db` (Postgres with pgvector), `/data/index` (retrieval index files), `/data/logs` (chat + UI event logs), and `/models` (Ollama model cache shared with the API).
- Default service ports inside the network: API `8000`, UI `80`, Postgres `5432`, Redis `6379`, Ollama `11434`; only ports `80/443` are published externally by the proxy.
- To stop the stack run `docker compose down` (add `--volumes` if you want to wipe the persisted data).
- For fast iteration use the dev override: `./scripts/docker-up.ssh --dev` mounts `./app`, `./data`, and `./models` into the containers so backend changes hot-reload without rebuilding.

## Local development

1. (Optional) `python3 -m venv .venv && source .venv/bin/activate` if you prefer manual control.
2. Run `./start.ssh` to bootstrap dependencies, launch the FastAPI backend on `http://127.0.0.1:8000`, and serve the widget assets on `http://127.0.0.1:4173` (visit `/test-host.html` to try the floating widget).
3. In another terminal, run `./start-fe.ssh` to install npm dependencies if needed and start the Vite dev server on `http://127.0.0.1:5173`.
4. Stop either process with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

### Customising ports/hosts

- Export `API_HOST`, `API_PORT`, `WIDGET_HOST`, or `WIDGET_PORT` before running `./start.ssh` to adjust where the backend and widget assets listen.
- Export `FE_HOST`, `FE_PORT`, or `VITE_API_BASE_URL` before running `./start-fe.ssh` to change the UI dev server host/port or point the UI at a different API.



### For personal reference CODEX DO NOT MODIFY
volumes - /data,  db index logs models
Only index and logs being used at this point of dockerization

Redis needs to be implemented
