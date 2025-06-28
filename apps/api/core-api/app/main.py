import os

# ✅ Ensure the tmp folder exists before mounting
tmp_dir = "D:/Games/GTA5/LermoAI-main/LermoAI-main/tmp"
os.makedirs(tmp_dir, exist_ok=True)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.api import ping, main
from app.engine import init_engine, config_agent

app = FastAPI()

# ✅ Configure CORS
origins = [
    "*",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

# ✅ Mount the tmp directory after ensuring it exists
app.mount("/tmp", StaticFiles(directory=tmp_dir), name="tmp")

# ✅ App startup and shutdown events
@app.on_event("startup")
async def startup():
    init_engine()
    config_agent()
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")

# ✅ API routes
app.include_router(ping.router)
app.include_router(main.router)
