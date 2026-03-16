from fastapi import FastAPI
from backend.api import router as api_router
from backend.api import chat as chat_router
from backend.api import lsp_proxy as lsp_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Repo Rosetta API", version="1.0.0")

app.include_router(api_router.router, prefix="/api")
app.include_router(chat_router.router, prefix="/api")
app.include_router(lsp_router.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Repo Rosetta API"}
