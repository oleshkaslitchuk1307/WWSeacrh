import sqlite3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from data_base import init_db
from container import Container

app = FastAPI(title='GameSearchSite', version='1.0.0')

init_db()
container = Container()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(sqlite3.IntegrityError)
async def integrity_error_handler(request: Request, exc: sqlite3.IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Такий запис вже існує"}
    )

app.include_router(container.actions_controller.router)
app.include_router(container.auth_controller.router)
app.include_router(container.chat_controller.router)
app.include_router(container.games_controller.router)
app.include_router(container.search_controller.router)
app.include_router(container.sharing_controller.router)
app.include_router(container.user_controller.router)

import os
from fastapi.responses import FileResponse

app.mount("/assets", StaticFiles(directory="client/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_spa(request: Request, full_path: str):
    # Serve index.html for all non-API paths
    index_path = os.path.join("client", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "Not found"})
