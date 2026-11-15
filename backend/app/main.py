"""API REST /api/v1; navegador consome API com cookies HttpOnly e CSRF."""
import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from .routers import auth, projects, resources

app=FastAPI(title="Requisitos Ágeis API",description="Protótipo acadêmico - 19 requisitos",version="1.0.0")
allowed=os.getenv("ALLOWED_ORIGINS","http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(CORSMiddleware,allow_origins=allowed,allow_credentials=True,allow_methods=["GET","POST","PATCH","PUT","DELETE"],allow_headers=["Content-Type","X-CSRF-Token"])
app.include_router(auth.router,prefix="/api/v1")
app.include_router(projects.router,prefix="/api/v1")
app.include_router(resources.router,prefix="/api/v1")

@app.get("/api/v1/health")
def health():
    return {"status":"ok","service":"Requisitos Ágeis","version":"1.0.0"}

@app.exception_handler(IntegrityError)
async def integrity_error(request:Request,exc:IntegrityError):
    # Não divulga dados, chaves ou nomes internos do banco.
    return JSONResponse(status_code=409,content={"detail":"A operação violou uma regra de integridade dos dados."})

# Deployment opcional: depois de npm run build, FastAPI pode servir o frontend compilado.
dist=Path(__file__).resolve().parents[2]/"frontend"/"dist"
if dist.is_dir():
    app.mount("/assets",StaticFiles(directory=dist/"assets"),name="assets")
    @app.get("/{path:path}",include_in_schema=False)
    async def spa(path:str):
        if path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Rota não encontrada.")
        file=(dist/path).resolve()
        if file.is_file() and file.is_relative_to(dist.resolve()):
            return FileResponse(file)
        return FileResponse(dist/"index.html")
