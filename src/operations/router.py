import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["operation"]
)

@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Для примера работы redis"

@router.get("/")
async def get_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.__table__.c.type == operation_type)
        res = await session.execute(query)
        return {
            "status": "success",
            "data": res.scalars().all(),
            "deatails": None
        }
    except ZeroDivisionError:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Ошибка! Деление на ноль."
        })
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.post("/")
async def add_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Operation).values(**new_operation.dict())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}