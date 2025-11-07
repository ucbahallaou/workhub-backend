from fastapi import FastAPI
from app.api.routers.health import router as health_router

app = FastAPI(title="WorkHub Backend", version="0.1.0")
app.include_router(health_router)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}
