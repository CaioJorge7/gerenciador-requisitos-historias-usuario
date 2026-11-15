$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $Root 'backend')
& '.\.venv\Scripts\python.exe' -m pytest -q
