from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.core.auth import get_current_user
from src.modules.user.models import User
from src.modules.vehicle.models import (
    VehicleListing, VehicleListingPhoto, VehicleGalleryCompany,
    VehicleFavoriteListing, VehicleInquiry,
)

router = APIRouter(prefix="/vehicles", tags=["vehicle-listings"])


# --- Gallery Companies ---

@router.post("/galleries", status_code=201)
async def create_gallery(
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    try:
        g = VehicleGalleryCompany(user_id=user.id, **data)
        db.add(g)
        await db.flush()
        await db.commit()
        return g
    except Exception as e:
        await db.rollback()
        raise HTTPException(400, str(e))


@router.get("/galleries", status_code=200)
async def list_galleries(db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(VehicleGalleryCompany).where(VehicleGalleryCompany.is_active == True)
        .order_by(VehicleGalleryCompany.rating.desc())
    )
    return r.scalars().all()


@router.get("/galleries/{gallery_id}", status_code=200)
async def get_gallery(gallery_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(VehicleGalleryCompany).where(VehicleGalleryCompany.id == gallery_id))
    g = r.scalar_one_or_none()
    if not g:
        raise HTTPException(404, "Galeri bulunamadı")
    return g


# --- Listings ---

@router.post("/listings", status_code=201)
async def create_listing(
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    listing = VehicleListing(user_id=user.id, **data)
    db.add(listing)
    await db.flush()
    await db.commit()
    return listing


@router.put("/listings/{listing_id}")
async def update_listing(
    listing_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(select(VehicleListing).where(VehicleListing.id == listing_id))
    listing = r.scalar_one_or_none()
    if not listing:
        raise HTTPException(404, "İlan bulunamadı")
    if listing.user_id != user.id:
        raise HTTPException(403, "Bu ilanı düzenleme yetkiniz yok")
    for k, v in data.items():
        setattr(listing, k, v)
    await db.commit()
    return listing


@router.get("/listings/{listing_id}")
async def get_listing(listing_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(VehicleListing).where(VehicleListing.id == listing_id, VehicleListing.is_active == True)
    )
    listing = r.scalar_one_or_none()
    if not listing:
        raise HTTPException(404, "İlan bulunamadı")
    listing.view_count = (listing.view_count or 0) + 1
    await db.commit()
    return listing


@router.delete("/listings/{listing_id}")
async def delete_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(select(VehicleListing).where(VehicleListing.id == listing_id))
    listing = r.scalar_one_or_none()
    if not listing:
        raise HTTPException(404, "İlan bulunamadı")
    if listing.user_id != user.id:
        raise HTTPException(403, "Yetkiniz yok")
    listing.is_active = False
    await db.commit()
    return {"status": "deleted"}


@router.get("/listings")
async def search_listings(
    brand_id: int | None = None,
    model_id: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    fuel_type: str | None = None,
    transmission: str | None = None,
    city: str | None = None,
    condition: str | None = None,
    sort: str = "newest",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    q = select(VehicleListing).where(VehicleListing.is_active == True, VehicleListing.status == "active")

    if brand_id:
        q = q.where(VehicleListing.brand_id == brand_id)
    if model_id:
        q = q.where(VehicleListing.model_id == model_id)
    if min_year:
        q = q.where(VehicleListing.year >= min_year)
    if max_year:
        q = q.where(VehicleListing.year <= max_year)
    if min_price is not None:
        q = q.where(VehicleListing.price >= min_price)
    if max_price is not None:
        q = q.where(VehicleListing.price <= max_price)
    if fuel_type:
        q = q.where(VehicleListing.fuel_type == fuel_type)
    if transmission:
        q = q.where(VehicleListing.transmission == transmission)
    if city:
        q = q.where(VehicleListing.city == city)
    if condition:
        q = q.where(VehicleListing.condition == condition)

    if sort == "price_asc":
        q = q.order_by(VehicleListing.price.asc())
    elif sort == "price_desc":
        q = q.order_by(VehicleListing.price.desc())
    elif sort == "year_desc":
        q = q.order_by(VehicleListing.year.desc())
    elif sort == "year_asc":
        q = q.order_by(VehicleListing.year.asc())
    elif sort == "mileage_asc":
        q = q.order_by(VehicleListing.mileage.asc().nullslast())
    else:
        q = q.order_by(VehicleListing.created_at.desc())

    cnt = await db.execute(select(func.count()).select_from(q.subquery()))
    total = cnt.scalar() or 0
    q = q.offset((page - 1) * limit).limit(limit)
    r = await db.execute(q)
    return {"items": r.scalars().all(), "total": total}


# --- Photos ---

@router.post("/listings/{listing_id}/photos", status_code=201)
async def add_photo(
    listing_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(select(VehicleListing).where(VehicleListing.id == listing_id))
    listing = r.scalar_one_or_none()
    if not listing or listing.user_id != user.id:
        raise HTTPException(403, "Yetkiniz yok")
    photo = VehicleListingPhoto(listing_id=listing_id, **data)
    db.add(photo)
    await db.commit()
    return photo


@router.get("/listings/{listing_id}/photos")
async def list_photos(listing_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(VehicleListingPhoto).where(VehicleListingPhoto.listing_id == listing_id)
        .order_by(VehicleListingPhoto.sort_order)
    )
    return r.scalars().all()


@router.delete("/photos/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(select(VehicleListingPhoto).where(VehicleListingPhoto.id == photo_id))
    photo = r.scalar_one_or_none()
    if not photo:
        raise HTTPException(404, "Fotoğraf bulunamadı")
    r2 = await db.execute(select(VehicleListing).where(VehicleListing.id == photo.listing_id))
    listing = r2.scalar_one_or_none()
    if not listing or listing.user_id != user.id:
        raise HTTPException(403, "Yetkiniz yok")
    await db.delete(photo)
    await db.commit()
    return {"status": "deleted"}


# --- Favorites ---

@router.post("/listings/{listing_id}/favorite")
async def add_favorite(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(
        select(VehicleFavoriteListing).where(
            VehicleFavoriteListing.user_id == user.id,
            VehicleFavoriteListing.listing_id == listing_id,
        )
    )
    if r.scalar_one_or_none():
        return {"status": "already_favorited"}
    fav = VehicleFavoriteListing(user_id=user.id, listing_id=listing_id)
    db.add(fav)
    await db.commit()
    return {"status": "favorited"}


@router.delete("/listings/{listing_id}/favorite")
async def remove_favorite(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(
        select(VehicleFavoriteListing).where(
            VehicleFavoriteListing.user_id == user.id,
            VehicleFavoriteListing.listing_id == listing_id,
        )
    )
    fav = r.scalar_one_or_none()
    if not fav:
        raise HTTPException(404, "Favorilerde bulunamadı")
    await db.delete(fav)
    await db.commit()
    return {"status": "removed"}


@router.get("/favorites")
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(
        select(VehicleListing).join(VehicleFavoriteListing)
        .where(VehicleFavoriteListing.user_id == user.id, VehicleListing.is_active == True)
    )
    return r.scalars().all()


# --- Inquiries ---

@router.post("/listings/{listing_id}/inquiry")
async def send_inquiry(
    listing_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(
        select(VehicleListing).where(VehicleListing.id == listing_id, VehicleListing.is_active == True)
    )
    if not r.scalar_one_or_none():
        raise HTTPException(404, "İlan bulunamadı")
    inquiry = VehicleInquiry(listing_id=listing_id, sender_id=user.id, message=data.get("message", ""))
    db.add(inquiry)
    await db.commit()
    return {"status": "inquiry_sent"}


@router.get("/listings/{listing_id}/inquiries")
async def list_inquiries(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    r = await db.execute(
        select(VehicleInquiry).where(VehicleInquiry.listing_id == listing_id)
        .order_by(VehicleInquiry.created_at.desc())
    )
    return r.scalars().all()
