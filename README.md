# sprint-marketing-bot
AI Agent for Sprint that is going to be a foundational basis for further modules

## Local development

1. (Optional) `python3 -m venv .venv && source .venv/bin/activate` if you prefer manual control.
2. Run `./start.ssh` to bootstrap dependencies, launch the FastAPI backend on `http://127.0.0.1:8000`, and serve the widget assets on `http://127.0.0.1:4173` (visit `/test-host.html` to try the floating widget).
3. In another terminal, run `./start-fe.ssh` to install npm dependencies if needed and start the Vite dev server on `http://127.0.0.1:5173`.
4. Stop either process with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

### Customising ports/hosts

- Export `API_HOST`, `API_PORT`, `WIDGET_HOST`, or `WIDGET_PORT` before running `./start.ssh` to adjust where the backend and widget assets listen.
- Export `FE_HOST`, `FE_PORT`, or `VITE_API_BASE_URL` before running `./start-fe.ssh` to change the UI dev server host/port or point the UI at a different API.
