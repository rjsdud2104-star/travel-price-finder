"""Travel Price Finder — FastAPI server."""
from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from src.models import SearchRequest
from src.search_engine import search, get_destinations

app = FastAPI(title="Travel Price Finder")
WEB = Path(__file__).parent / "web"

@app.get("/")
async def index():
    return FileResponse(WEB / "index.html")

@app.post("/api/search")
async def api_search(req: SearchRequest):
    result = search(req)
    return result.model_dump()

@app.get("/api/destinations")
async def api_destinations(category: str | None = None, q: str | None = None):
    dests = get_destinations(category, q)
    return [d.model_dump() for d in dests]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
