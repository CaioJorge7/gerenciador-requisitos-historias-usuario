$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $Root 'backend')
if (!(Test-Path '.venv\Scripts\python.exe')) { throw 'Execute scripts\instalar_windows.ps1 antes.' }
& '.\.venv\Scripts\python.exe' -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
