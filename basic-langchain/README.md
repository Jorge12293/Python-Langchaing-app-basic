// Active Environment
source .venv/bin/activate
// deactivate Environment
deactivate

// Init venv
rm -rf .venv
python3 -m venv .venv

// Volver a instalar
uv sync
