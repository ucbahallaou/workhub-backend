import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.db.base import Base  # <-- use the single source of truth

def _ssl_args():
    mode = settings.db_ssl_mode.lower()
    if mode == "disable":
        return {}
    if mode == "require":
        return {"ssl": ssl.create_default_context()}
    if mode == "verify-full":
        ctx = ssl.create_default_context()
        # Optionally: ctx.load_verify_locations(cafile="app/certs/supabase-ca.crt")
        return {"ssl": ctx}
    return {}

engine = create_async_engine(
    str(settings.database_url),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=_ssl_args(),
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
