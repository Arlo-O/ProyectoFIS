# Start development script for ProyectoFIS (PowerShell)
param(
    [switch]$createTables
)

Write-Host "Ensure virtual environment .venv exists and activate it..."
# Create venv if missing
if (-not (Test-Path .\.venv)) {
    Write-Host "Virtual environment not found — creating .venv..."
    python -m venv .venv
}

# On Windows PowerShell, execution policy may block Activate.ps1; set bypass for this process
try {
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force | Out-Null
} catch {
    Write-Host "Warning: could not set ExecutionPolicy for process. You may need to run PowerShell as Administrator or activate manually." -ForegroundColor Yellow
}

if (Test-Path .\.venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
} elseif (Test-Path .\.venv\Scripts\activate) {
    # fallback for non-PowerShell shells
    . .\.venv\Scripts\activate
} else {
    Write-Host "Failed to find activation script in .venv\Scripts. You may need to create venv manually: python -m venv .venv" -ForegroundColor Red
}

Write-Host "Installing requirements (if needed)..."
pip install -r requirements.txt

Write-Host "Registering mappers..."
python - <<'PY'
from app.infraestructura.mappers import start_mappers
start_mappers()
print('Mappers registered')
PY

if ($createTables) {
    Write-Host "Creating DB tables from metadata (development only)..."
    python - <<'PY'
from app.infraestructura.db import mapper_registry, engine
mapper_registry.metadata.create_all(bind=engine)
print('Tables created (if not existed)')
PY
}

Write-Host "Starting application..."
python run_app.py
