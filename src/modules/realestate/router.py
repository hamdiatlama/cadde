from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user

router = APIRouter(prefix="/realestate", tags=["realestate"])


# ── Categories ──────────────────────────────────────────────

@router.get("/categories", response_model=list[dict])
async def list_categories(db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_categories()


@router.post("/categories", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_category(data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Types ───────────────────────────────────────────────────

@router.get("/types", response_model=list[dict])
async def list_types(db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_types()


@router.post("/types", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_type(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_type(data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Listings ────────────────────────────────────────────────

@router.post("/listings", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_listing(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_listing(current_user.id, data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/listings/price")
async def get_listing_price(
    domain: str = Query("realestate"),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    result = await svc.get_listing_price(domain)
    if not result:
        raise HTTPException(status_code=404, detail="Price config not found")
    return result


@router.get("/listings", response_model=dict)
async def list_listings(
    category: int = Query(None),
    type: int = Query(None, alias="type_id"),
    city: str = Query(None),
    district: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    room: str = Query(None, alias="room_count"),
    status: str = Query(None),
    sort: str = Query("-created_at", alias="sort_by"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    filters = {k: v for k, v in {
        "category_id": category,
        "type_id": type,
        "city": city,
        "district": district,
        "min_price": min_price,
        "max_price": max_price,
        "room_count": room,
        "status": status,
        "sort_by": sort,
    }.items() if v is not None}
    result = await svc.search_with_filters(q, filters, page, limit)
    return result


@router.get("/listings/{listing_id}", response_model=dict)
async def get_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.increment_view_count(listing_id)
    result = await svc.get_listing_detail(listing_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Listing not found")
    return result


@router.get("/listings/{listing_id}/public", response_model=dict)
async def get_listing_public(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.increment_view_count(listing_id)
    result = await svc.get_listing(listing_id)
    if not result:
        raise HTTPException(status_code=404, detail="Listing not found")
    return result


@router.put("/listings/{listing_id}", response_model=dict)
async def update_listing(
    listing_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.update_listing(listing_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/listings/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        await svc.delete_listing(listing_id, current_user.id)
        await db.commit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Photos ──────────────────────────────────────────────────

@router.post("/listings/{listing_id}/photos", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_photo(
    listing_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.add_photo(listing_id, data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/listings/{listing_id}/photos", response_model=list[dict])
async def list_photos(listing_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_photos(listing_id)


@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        await svc.delete_photo(photo_id)
        await db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/photos/{photo_id}/cover", response_model=dict)
async def set_cover_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        await svc.set_cover_photo(photo_id)
        await db.commit()
        return {"status": "cover_updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Features ────────────────────────────────────────────────

@router.get("/features", response_model=list[dict])
async def list_features(
    category: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_features(category)


@router.post("/features", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_feature(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_feature(data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/listings/{listing_id}/features", response_model=dict)
async def add_listing_features(
    listing_id: int,
    features: list[dict],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    result = await svc.add_listing_features(listing_id, features)
    await db.commit()
    return result


@router.get("/listings/{listing_id}/features", response_model=list[dict])
async def get_listing_features(listing_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.get_listing_features(listing_id)


@router.delete("/listings/{listing_id}/features/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_listing_feature(
    listing_id: int,
    feature_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.remove_listing_feature(listing_id, feature_id)
    await db.commit()


# ── Inquiries ───────────────────────────────────────────────

@router.post("/listings/{listing_id}/inquiry", response_model=dict, status_code=status.HTTP_201_CREATED)
async def send_inquiry(
    listing_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    data["listing_id"] = listing_id
    data["from_user_id"] = current_user.id
    result = await svc.send_inquiry(data)
    await db.commit()
    return result


@router.get("/listings/{listing_id}/inquiries", response_model=list[dict])
async def list_inquiries(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_inquiries(listing_id=listing_id)


@router.get("/listings/{listing_id}/land-contents", response_model=list[dict])
async def list_land_contents(listing_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_land_contents(listing_id)


@router.post("/listings/{listing_id}/land-contents", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_land_content(
    listing_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    data["listing_id"] = listing_id
    result = await svc.create_land_content(data)
    await db.commit()
    return result


@router.put("/land-contents/{content_id}", response_model=dict)
async def update_land_content(
    content_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.update_land_content(content_id, data)
    await db.commit()
    return {"status": "updated"}


@router.delete("/land-contents/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_land_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.delete_land_content(content_id)
    await db.commit()


@router.put("/inquiries/{inquiry_id}/read", response_model=dict)
async def mark_inquiry_read(
    inquiry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.mark_as_read(inquiry_id)
    await db.commit()
    return {"status": "read"}


# ── Favorites ───────────────────────────────────────────────

@router.post("/listings/{listing_id}/favorite", response_model=dict)
async def add_favorite(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    result = await svc.add_favorite(current_user.id, listing_id)
    await db.commit()
    return result


@router.delete("/listings/{listing_id}/favorite", response_model=dict)
async def remove_favorite(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    await svc.remove_favorite(current_user.id, listing_id)
    await db.commit()
    return {"status": "removed"}


# ── Listing Pricing / Payments ─────────────────────────────────


@router.post("/listings/{listing_id}/pay", response_model=dict)
async def pay_for_listing(
    listing_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.pay_for_listing(
            domain=data.get("domain", "realestate"),
            listing_id=listing_id,
            user_id=current_user.id,
            payment_method=data.get("payment_method", "balance"),
            user_role=current_user.role,
        )
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/listings/{listing_id}/benchmark", response_model=dict)
async def get_listing_benchmark(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    result = await svc.calculate_region_benchmark(listing_id)
    if not result:
        raise HTTPException(status_code=404, detail="Listing not found")
    return result


@router.get("/payments", response_model=list[dict])
async def list_my_payments(
    domain: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    payments = await svc.repo.list_user_payments(current_user.id, domain)
    return [
        {
            "id": p.id,
            "domain": p.domain,
            "listing_id": p.listing_id,
            "amount": str(p.amount),
            "currency": p.currency,
            "payment_method": p.payment_method,
            "payment_ref": p.payment_ref,
            "status": p.status,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in payments
    ]


@router.get("/favorites", response_model=list[dict])
async def list_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_favorites(current_user.id)


# ── Documents ────────────────────────────────────────────────

@router.post("/listings/{listing_id}/documents", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_document(
    listing_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.upload_document(
            domain=data.get("domain", "realestate"),
            listing_id=listing_id,
            user_id=current_user.id,
            data=data,
        )
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/listings/{listing_id}/documents", response_model=list[dict])
async def list_listing_documents(
    listing_id: int,
    domain: str = Query("realestate"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.get_listing_documents(domain, listing_id)


@router.post("/listings/{listing_id}/submit-verification", response_model=dict)
async def submit_for_verification(
    listing_id: int,
    data: dict = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    domain = (data or {}).get("domain", "realestate")
    try:
        result = await svc.submit_for_verification(domain, listing_id, current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/documents/{doc_id}/verify", response_model=dict)
async def verify_document(
    doc_id: int,
    data: dict = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    reason = (data or {}).get("reason")
    try:
        result = await svc.verify_document(doc_id, current_user.id, "verify", reason)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/documents/{doc_id}/reject", response_model=dict)
async def reject_document(
    doc_id: int,
    data: dict = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    reason = (data or {}).get("reason")
    try:
        result = await svc.verify_document(doc_id, current_user.id, "reject", reason)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-documents", response_model=list[dict])
async def my_documents(
    domain: str = Query("realestate"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.get_user_documents(current_user.id, domain)


# ── Contractors ─────────────────────────────────────────────

@router.post("/contractors", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_company(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_company(data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contractors", response_model=list[dict])
async def list_companies(
    q: str = Query(None),
    is_verified: bool = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_companies(q, is_verified)


@router.get("/contractors/{company_id}", response_model=dict)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    result = await svc.get_company(company_id)
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return result


@router.post("/contractors/{company_id}/reviews", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_review(
    company_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_review(company_id, current_user.id, data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contractors/{company_id}/reviews", response_model=list[dict])
async def list_reviews(company_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_reviews(company_id)


# ── Company Documents ───────────────────────────────────────

@router.post("/contractors/{company_id}/documents", response_model=dict, status_code=status.HTTP_201_CREATED)
async def upload_company_document(
    company_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.upload_company_document(company_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contractors/{company_id}/documents", response_model=list[dict])
async def list_company_documents(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_company_documents(company_id)


@router.post("/contractors/{company_id}/submit-verification", response_model=dict)
async def submit_company_verification(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.submit_company_for_verification(company_id, current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/contractors/{company_id}/verify", response_model=dict)
async def verify_company(
    company_id: int,
    data: dict = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    reason = (data or {}).get("reason")
    try:
        result = await svc.verify_company(company_id, current_user.id, "verify", reason)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/contractors/{company_id}/reject", response_model=dict)
async def reject_company(
    company_id: int,
    data: dict = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    reason = (data or {}).get("reason")
    try:
        result = await svc.verify_company(company_id, current_user.id, "reject", reason)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admin/pending-companies", response_model=list[dict])
async def pending_verification_companies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.repo.get_pending_verification_companies()


# ── Company Members ─────────────────────────────────────────

@router.post("/contractors/{company_id}/members", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_member(
    company_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_member(company_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contractors/{company_id}/members", response_model=list[dict])
async def list_members(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_members(company_id)


@router.put("/members/{member_id}", response_model=dict)
async def update_member_role(
    member_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.update_member_role(member_id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    member_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        await svc.remove_member(member_id)
        await db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Company Invitations ─────────────────────────────────────

@router.post("/contractors/{company_id}/invitations", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_invitation(
    company_id: int,
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_invitation(company_id, current_user.id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contractors/{company_id}/invitations", response_model=list[dict])
async def list_invitations(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_invitations(company_id)


@router.post("/invitations/{invitation_id}/accept", response_model=dict)
async def accept_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.respond_to_invitation(invitation_id, current_user.id, accept=True)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/invitations/{invitation_id}/reject", response_model=dict)
async def reject_invitation(
    invitation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.respond_to_invitation(invitation_id, current_user.id, accept=False)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-companies", response_model=list[dict])
async def my_companies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.get_user_companies(current_user.id)


# ── Authorizations ──────────────────────────────────────────

@router.post("/authorizations", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_authorization(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_authorization(data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/authorizations", response_model=list[dict])
async def list_authorizations(
    owner_id: int = Query(None),
    company_id: int = Query(None),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_authorizations(owner_id, company_id, status)


@router.put("/authorizations/{auth_id}/status", response_model=dict)
async def update_authorization_status(
    auth_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.update_authorization_status(auth_id, status)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Appraisals ──────────────────────────────────────────────

@router.post("/appraisals", response_model=dict, status_code=status.HTTP_201_CREATED)
async def request_appraisal(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.create_appraisal_request(current_user.id, data)
        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/appraisals", response_model=list[dict])
async def list_appraisals(
    user_id: int = Query(None),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    return await svc.list_appraisal_requests(user_id or current_user.id, status)


@router.get("/appraisals/{appraisal_id}", response_model=dict)
async def get_appraisal(
    appraisal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    result = await svc.get_appraisal_request(appraisal_id)
    if not result:
        raise HTTPException(status_code=404, detail="Appraisal request not found")
    return result


@router.put("/appraisals/{appraisal_id}/status", response_model=dict)
async def update_appraisal_status(
    appraisal_id: int,
    status: str,
    report_data: dict = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.modules.realestate.service import RealEstateService
    svc = RealEstateService(db)
    try:
        result = await svc.update_appraisal_status(appraisal_id, status, report_data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
