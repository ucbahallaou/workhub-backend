from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health():
    return {"ok": True}

@router.get("/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    # Simple connectivity check
    result = await session.execute(text("select 1"))
    one = result.scalar_one()
    return {"db_ok": one == 1}
