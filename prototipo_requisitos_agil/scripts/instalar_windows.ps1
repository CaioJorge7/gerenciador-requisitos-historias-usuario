$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Write-Host '[1/4] Preparando ambiente Python...' -ForegroundColor Cyan
Set-Location (Join-Path $Root 'backend')
if (!(Test-Path '.venv')) { py -3.12 -m venv .venv }
& '.\.venv\Scripts\python.exe' -m pip install --upgrade pip
& '.\.venv\Scripts\python.exe' -m pip install -r requirements-dev.txt
if (!(Test-Path '.env')) {
  Copy-Item '.env.example' '.env'
  Write-Warning 'Edite backend\.env com DATABASE_URL e APP_SECRET_KEY antes de executar as migrações!'
}
Write-Host '[2/4] Dependências JavaScript...' -ForegroundColor Cyan
Set-Location (Join-Path $Root 'frontend')
npm install
Write-Host '[3/4] Migrações (requer PostgreSQL já configurado)...' -ForegroundColor Cyan
Set-Location (Join-Path $Root 'backend')
Write-Host 'Depois de configurar o .env, execute:' -ForegroundColor Yellow
Write-Host '  .\.venv\Scripts\python.exe -m alembic upgrade head'
Write-Host '[4/4] Pronto. Consulte o README.md para iniciar o backend e o frontend.' -ForegroundColor Green
