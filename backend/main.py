from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.database import init_db
from backend.routers import hands, imports
from backend.routers import hands, imports, stats

app = FastAPI(title="Grindset API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(hands.router)
app.include_router(imports.router)
app.include_router(stats.router)

@app.get("/")
def home():
    return {"message": "Grindset API is running"}

@app.get("/status")
def status():
    return {"status": "ok", "version": "1.0"}