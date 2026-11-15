$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $Root 'frontend')
npm install
npm run build
Write-Host 'Frontend compilado em frontend\dist.' -ForegroundColor Green
Write-Host 'Agora o FastAPI pode servir o frontend pela URL http://127.0.0.1:8000.'
