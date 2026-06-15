from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.warehouse.repository import WarehouseRepository

router = APIRouter(prefix="/warehouse", tags=["warehouse"])


@router.post("", status_code=201)
async def create_warehouse(name: str, address: str = None, city: str = None,
                            current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    w = await repo.create_warehouse(current_user.id, name, address, city)
    await db.commit()
    return {"id": w.id, "name": w.name}


@router.get("")
async def list_warehouses(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    return await repo.list_warehouses(current_user.id)


@router.post("/stock", status_code=201)
async def set_stock(warehouse_id: int, product_id: int, quantity: int, sku_id: int = None,
                     current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    ws = await repo.set_stock(warehouse_id, product_id, quantity, sku_id)
    await db.commit()
    return {"warehouse_id": warehouse_id, "product_id": product_id, "quantity": ws.quantity}


@router.get("/stock")
async def get_stock(product_id: int = None, warehouse_id: int = None,
                     current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    return await repo.get_stock(warehouse_id, product_id)


@router.get("/stock/total/{product_id}")
async def total_stock(product_id: int, sku_id: int = None, db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    total = await repo.total_stock(product_id, sku_id)
    return {"product_id": product_id, "sku_id": sku_id, "total_stock": total}


@router.post("/transfer", status_code=201)
async def transfer_stock(from_warehouse_id: int, to_warehouse_id: int, product_id: int, quantity: int,
                          current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    t = await repo.create_transfer(from_warehouse_id, to_warehouse_id, product_id, quantity)
    await db.commit()
    return {"id": t.id, "status": t.status}


@router.get("/alerts")
async def low_stock_alerts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WarehouseRepository(db)
    return await repo.create_low_stock_alert(current_user.id)
