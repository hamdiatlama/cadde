from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.core.auth import get_current_user
from src.modules.user.models import User
from src.modules.cicek.schemas import (
    FloristProfileCreate, FloristProfileUpdate, FloristProfileResponse, FloristPublicResponse,
    FlowerProductCreate, FlowerProductUpdate, FlowerProductResponse,
    SpecialDayReminderCreate, SpecialDayReminderResponse,
    CustomOrderDesignCreate, CustomOrderDesignResponse,
    FloristStatusResponse, FloristImageCreate, FloristDocumentCreate,
    FlowerRatingCreate, FreshnessRecordCreate,
)
from src.modules.cicek.service import FloristService

router = APIRouter(prefix="/cicek", tags=["cicek"])


def _svc(db: AsyncSession = Depends(get_db)) -> FloristService:
    return FloristService(db)


# --- Florist Profile ---

@router.post("/florists", response_model=dict)
async def register_florist(
    data: FloristProfileCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    result = await svc.register(user.id, data)
    if "error" in result:
        raise HTTPException(400, result["error"])
    await db.commit()
    return result


@router.get("/florists/me", response_model=FloristProfileResponse | None)
async def my_florist(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    return await svc.get_my_shop(user.id)


@router.get("/florists/{florist_id}", response_model=FloristProfileResponse)
async def get_florist(
    florist_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    f = await svc.get_shop(florist_id)
    if not f:
        raise HTTPException(404, "Çiçekçi bulunamadı")
    return f


@router.put("/florists/{florist_id}", response_model=dict)
async def update_florist(
    florist_id: int,
    data: FloristProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    result = await svc.update_shop(florist_id, user.id, data)
    if not result:
        raise HTTPException(404, "Çiçekçi bulunamadı veya yetkiniz yok")
    await db.commit()
    return result


@router.post("/florists/{florist_id}/toggle")
async def toggle_florist(
    florist_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    result = await svc.toggle_open(florist_id, user.id)
    if not result:
        raise HTTPException(404, "Çiçekçi bulunamadı veya yetkiniz yok")
    await db.commit()
    return result


# --- Public ---

@router.get("/public/florists", response_model=list[FloristPublicResponse])
async def list_florists(
    city: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    svc = FloristService(db)
    items, total = await svc.list_florists(city, page, limit)
    return items


@router.get("/public/florists/{slug}", response_model=FloristPublicResponse)
async def get_florist_public(slug: str, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    f = await svc.get_shop_by_slug(slug)
    if not f:
        raise HTTPException(404, "Çiçekçi bulunamadı")
    return f


@router.get("/public/florists/{florist_id}/products", response_model=list[FlowerProductResponse])
async def list_florist_products(
    florist_id: int,
    category: str | None = None,
    occasion: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    svc = FloristService(db)
    items, total = await svc.list_products("florist", florist_id, category, occasion, page, limit)
    return items


# --- Products ---

@router.post("/florists/{florist_id}/products", response_model=FlowerProductResponse)
async def create_product(
    florist_id: int,
    data: FlowerProductCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    f = await svc.get_shop(florist_id)
    if not f or f.user_id != user.id:
        raise HTTPException(403, "Bu çiçekçiye ürün ekleme yetkiniz yok")
    p = await svc.create_product("florist", florist_id, data)
    await db.commit()
    return p


@router.put("/products/{product_id}", response_model=FlowerProductResponse)
async def update_product(
    product_id: int,
    data: FlowerProductUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    p = await svc.get_product(product_id)
    if not p:
        raise HTTPException(404, "Ürün bulunamadı")
    f = await svc.get_shop(p.seller_id)
    if not f or f.user_id != user.id:
        raise HTTPException(403, "Yetkiniz yok")
    result = await svc.update_product(product_id, p.seller_id, user.id, data)
    if not result:
        raise HTTPException(404, "Ürün güncellenemedi")
    await db.commit()
    return result


@router.get("/products/{product_id}", response_model=FlowerProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    p = await svc.get_product(product_id)
    if not p:
        raise HTTPException(404, "Ürün bulunamadı")
    return p


# --- Special Day Reminders ---

@router.post("/reminders", response_model=SpecialDayReminderResponse)
async def create_reminder(
    data: SpecialDayReminderCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    r = await svc.create_reminder(user.id, data)
    await db.commit()
    return r


@router.get("/reminders", response_model=list[SpecialDayReminderResponse])
async def list_reminders(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    return await svc.list_reminders(user.id)


@router.delete("/reminders/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    ok = await svc.delete_reminder(reminder_id, user.id)
    if not ok:
        raise HTTPException(404, "Hatırlatıcı bulunamadı")
    await db.commit()
    return {"status": "deleted"}


# --- Custom Order Design ---

@router.post("/designs", response_model=CustomOrderDesignResponse)
async def create_design(
    data: CustomOrderDesignCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    d = await svc.create_design(user.id, data)
    await db.commit()
    return d


@router.get("/designs/{design_id}", response_model=CustomOrderDesignResponse)
async def get_design(design_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    d = await svc.get_design(design_id)
    if not d:
        raise HTTPException(404, "Tasarım bulunamadı")
    return d


# --- Florist Images ---

@router.post("/florists/{florist_id}/images")
async def add_image(
    florist_id: int,
    data: FloristImageCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    img = await svc.add_image(florist_id, user.id, data)
    if not img:
        raise HTTPException(403, "Yetkiniz yok")
    await db.commit()
    return {"id": img.id, "category": img.category}


@router.get("/florists/{florist_id}/images")
async def list_images(florist_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    return await svc.list_images(florist_id)


@router.delete("/images/{image_id}")
async def delete_image(
    image_id: int,
    florist_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    ok = await svc.delete_image(image_id, florist_id, user.id)
    if not ok:
        raise HTTPException(404, "Görsel bulunamadı veya yetkiniz yok")
    await db.commit()
    return {"status": "deleted"}


# --- Cameras ---

@router.post("/florists/{florist_id}/cameras")
async def add_camera(
    florist_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    cam = await svc.add_camera(florist_id, user.id, data)
    if not cam:
        raise HTTPException(403, "Yetkiniz yok")
    await db.commit()
    return {"id": cam.id, "camera_name": cam.camera_name}


@router.get("/florists/{florist_id}/cameras")
async def list_cameras(florist_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    return await svc.list_cameras(florist_id)


# --- Freshness Chain ---

@router.post("/freshness")
async def add_freshness(
    data: FreshnessRecordCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    rec = await svc.add_freshness_record(data)
    await db.commit()
    return {"id": rec.id, "stage": rec.stage}


@router.get("/freshness/{order_id}")
async def get_freshness(order_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    return await svc.get_freshness_chain(order_id)


# --- Documents ---

@router.post("/florists/{florist_id}/documents")
async def add_document(
    florist_id: int,
    data: FloristDocumentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    doc = await svc.add_document(florist_id, user.id, data)
    if not doc:
        raise HTTPException(403, "Yetkiniz yok")
    await db.commit()
    return {"id": doc.id, "document_type": doc.document_type}


@router.get("/florists/{florist_id}/documents")
async def list_documents(florist_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    return await svc.list_documents(florist_id)


# --- Score ---

@router.post("/florists/{florist_id}/recalculate-score")
async def recalculate_score(
    florist_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    f = await svc.get_shop(florist_id)
    if not f or f.user_id != user.id:
        raise HTTPException(403, "Yetkiniz yok")
    total = await svc.total_score(florist_id)
    await db.commit()
    return {"florist_id": florist_id, "total_score": total}


# --- Ratings ---

@router.post("/ratings")
async def add_rating(
    data: FlowerRatingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FloristService(db)
    rat = await svc.add_rating(user.id, data)
    await db.commit()
    return {"id": rat.id, "score": rat.score}


# --- Status ---

@router.get("/florists/{florist_id}/status", response_model=FloristStatusResponse)
async def get_florist_status(florist_id: int, db: AsyncSession = Depends(get_db)):
    svc = FloristService(db)
    f = await svc.get_shop(florist_id)
    if not f:
        raise HTTPException(404, "Çiçekçi bulunamadı")
    if not f.is_active:
        return FloristStatusResponse(durum="pasif")
    if f.is_open:
        return FloristStatusResponse(durum="acik", calisma_saatleri=f.working_hours_json)
    return FloristStatusResponse(durum="calisma_saati_disi", calisma_saatleri=f.working_hours_json)
