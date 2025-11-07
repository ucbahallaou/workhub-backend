from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from app.api.routers.health import router as health_router
from app.api.routers.auth import router as auth_router
from app.db.session import engine
from app.db.base import Base  # metadata lives here

app = FastAPI(title="WorkHub Backend", version="0.1.0")
app.include_router(health_router)
app.include_router(auth_router)

@app.on_event("startup")
async def on_startup():
    # Bootstrap tables so you can run immediately; we'll swap to Alembic next.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}
