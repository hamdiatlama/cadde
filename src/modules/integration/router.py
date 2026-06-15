from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.integration.repository import ErpRepository

router = APIRouter(prefix="/integration", tags=["integration"])


@router.post("/erp", status_code=201)
async def connect_erp(data: dict, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    repo = ErpRepository(db)
    data["seller_id"] = current_user.id
    conn = await repo.connect(data)
    await db.commit()
    return {"id": conn.id, "erp_type": conn.erp_type, "company_id": conn.company_id}


@router.get("/erp")
async def list_connections(current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    repo = ErpRepository(db)
    return await repo.list_connections(current_user.id)


@router.post("/erp/{id}/sync")
async def sync_erp(id: int, sync_type: str = "products",
                   current_user: User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    repo = ErpRepository(db)
    try:
        log = await repo.sync(id, sync_type, current_user.id)
        await db.commit()
        return {"log_id": log.id, "sync_type": log.sync_type, "status": log.status,
                "records_synced": log.records_synced}
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/erp/{id}/logs")
async def get_sync_logs(id: int, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    repo = ErpRepository(db)
    return await repo.get_sync_logs(id)


@router.delete("/erp/{id}")
async def disconnect_erp(id: int, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    repo = ErpRepository(db)
    conn = await repo.disconnect(id, current_user.id)
    if not conn:
        raise HTTPException(404, "Connection not found")
    await db.commit()
    return {"message": "Disconnected", "id": id}
