from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.food.schemas import (
    RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate,
    ModifierCreate, BranchCreate, ZoneCreate, ChatSend,
    TemperatureLog, HygieneReportCreate, DriverReportCreate, BatchPreventCreate,
)
from src.modules.food.service import (
    RestaurantService, MenuService, ModifierService,
    BranchService, ZoneService, CourierFoodService, ChatService, QualityService,
)

router = APIRouter(prefix="/food", tags=["food"])


# ─── 1) RESTAURANT CRUD ─────────────────────────────

@router.post("/restaurants", response_model=dict, status_code=201)
async def register_restaurant(
    data: RestaurantCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers can register")
    svc = RestaurantService(db)
    try:
        result = await svc.register(current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/restaurants/{rest_id}", response_model=dict)
async def update_restaurant(
    rest_id: int, data: RestaurantUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = RestaurantService(db)
    try:
        result = await svc.update(rest_id, current_user.id, data.model_dump(exclude_unset=True))
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/restaurants/{rest_id}/verify")
async def verify_restaurant(
    rest_id: int, status: str = "verified", hygiene_rating: str = "A",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    svc = RestaurantService(db)
    try:
        result = await svc.verify(rest_id, status, hygiene_rating)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/restaurants", response_model=list[dict])
async def list_restaurants(
    cuisine_type: str = Query(None), cuisine_subtypes: str = Query(None),
    dietary: str = Query(None), verified_only: bool = Query(True),
    search: str = Query(None),
    latitude: float = Query(None), longitude: float = Query(None),
    radius_km: float = Query(None, ge=1, le=50),
    min_rating: float = Query(None, ge=0, le=5),
    is_open: bool = Query(None),
    min_price: float = Query(None, ge=0), max_price: float = Query(None, ge=0),
    sort_by: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = RestaurantService(db)
    return await svc.search(
        cuisine_type=cuisine_type, cuisine_subtypes=cuisine_subtypes,
        dietary=dietary, verified_only=verified_only, search=search,
        latitude=latitude, longitude=longitude, radius_km=radius_km,
        min_rating=min_rating, is_open=is_open,
        min_price=min_price, max_price=max_price, sort_by=sort_by,
    )


# ─── 2) MENU FULL CRUD ──────────────────────────────

@router.post("/menu", response_model=dict, status_code=201)
async def create_menu_item(
    data: MenuItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = MenuService(db)
    try:
        result = await svc.create_item(current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/menu/{item_id}", response_model=dict)
async def update_menu_item(
    item_id: int, data: MenuItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = MenuService(db)
    try:
        result = await svc.update_item(item_id, current_user.id, data.model_dump(exclude_unset=True))
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/menu/{item_id}", response_model=dict)
async def delete_menu_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = MenuService(db)
    try:
        result = await svc.delete_item(item_id, current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/menu/{rest_id}", response_model=list[dict])
async def get_menu(
    rest_id: int, category: str = Query(None),
    dietary: str = Query(None),
    min_price: float = Query(None, ge=0), max_price: float = Query(None, ge=0),
    search: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = MenuService(db)
    return await svc.get_menu(
        rest_id, category=category, dietary=dietary,
        min_price=min_price, max_price=max_price, search=search,
    )


# ─── 3) MODIFIERS ───────────────────────────────────

@router.post("/menu/{item_id}/modifiers", response_model=dict, status_code=201)
async def add_modifier(
    item_id: int, data: ModifierCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = ModifierService(db)
    try:
        result = await svc.add(item_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/modifiers/{mod_id}", response_model=dict)
async def delete_modifier(
    mod_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = ModifierService(db)
    try:
        result = await svc.delete(mod_id, current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 4) BRANCHES ────────────────────────────────────

@router.post("/restaurants/{rest_id}/branches", response_model=dict, status_code=201)
async def add_branch(
    rest_id: int, data: BranchCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = BranchService(db)
    try:
        result = await svc.add(rest_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/restaurants/{rest_id}/branches", response_model=list[dict])
async def list_branches(rest_id: int, db: AsyncSession = Depends(get_db)):
    svc = BranchService(db)
    return await svc.list(rest_id)


# ─── 5) DELIVERY ZONES ──────────────────────────────

@router.post("/restaurants/{rest_id}/zones", response_model=dict, status_code=201)
async def add_zone(
    rest_id: int, data: ZoneCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = ZoneService(db)
    try:
        result = await svc.add(rest_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/restaurants/{rest_id}/zones", response_model=list[dict])
async def list_zones(rest_id: int, db: AsyncSession = Depends(get_db)):
    svc = ZoneService(db)
    return await svc.list(rest_id)


# ─── 6) COURIER EARNINGS ────────────────────────────

@router.get("/courier/earnings", response_model=dict)
async def courier_earnings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Only couriers")
    svc = CourierFoodService(db)
    try:
        return await svc.get_earnings(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 7) COURIER SHIFT ───────────────────────────────

@router.post("/courier/shift/start", response_model=dict)
async def start_shift(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Only couriers")
    svc = CourierFoodService(db)
    try:
        result = await svc.start_shift(current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/courier/shift/end", response_model=dict)
async def end_shift(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Only couriers")
    svc = CourierFoodService(db)
    try:
        result = await svc.end_shift(current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── 8) CHAT ─────────────────────────────────────────

@router.post("/chat/{order_id}", response_model=dict, status_code=201)
async def send_chat_message(
    order_id: int, data: ChatSend,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ChatService(db)
    try:
        result = await svc.send(order_id, current_user.id, data.receiver_role, data.message)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/chat/{order_id}", response_model=list[dict])
async def get_chat_messages(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ChatService(db)
    try:
        return await svc.get_messages(order_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 9) TEMPERATURE CHECKS ─────────────────────────

@router.post("/temperature", response_model=dict)
async def log_temperature(
    data: TemperatureLog,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Only couriers")
    svc = QualityService(db)
    result = await svc.log_temperature(
        data.order_id, current_user.id, data.temperature_celsius,
        data.check_type, data.photo_url, data.notes,
    )
    await db.commit()
    return result


@router.get("/temperature/{order_id}", response_model=list[dict])
async def get_temperature_logs(order_id: int, db: AsyncSession = Depends(get_db)):
    svc = QualityService(db)
    return await svc.get_temperature_logs(order_id)


# ─── 10) HYGIENE REPORTS ────────────────────────────

@router.post("/hygiene-report", response_model=dict)
async def report_hygiene(
    data: HygieneReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = QualityService(db)
    result = await svc.report_hygiene(current_user.id, current_user.role, data)
    await db.commit()
    return result


@router.get("/hygiene-reports", response_model=list[dict])
async def list_hygiene_reports(
    status_filter: str = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    svc = QualityService(db)
    return await svc.list_hygiene_reports(status_filter)


# ─── 11) DRIVER REPORTS ─────────────────────────────

@router.post("/driver-report", response_model=dict)
async def report_driver(
    data: DriverReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = QualityService(db)
    result = await svc.report_driver(current_user.id, data)
    await db.commit()
    return result


@router.get("/driver-reports/{courier_id}", response_model=list[dict])
async def get_driver_reports(
    courier_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    svc = QualityService(db)
    return await svc.get_driver_reports(courier_id)


# ─── 12) BATCH DELIVERY PREVENTION ─────────────────

@router.post("/batch-prevent/{order_id}", response_model=dict)
async def prevent_batch(
    order_id: int, data: BatchPreventCreate = BatchPreventCreate(),
    db: AsyncSession = Depends(get_db),
):
    svc = QualityService(db)
    result = await svc.set_batch_prevention(order_id, data.max_batch_size)
    await db.commit()
    return result


@router.get("/batch-prevent/{order_id}", response_model=dict)
async def check_batch_prevention(order_id: int, db: AsyncSession = Depends(get_db)):
    svc = QualityService(db)
    return await svc.get_batch_prevention(order_id)
