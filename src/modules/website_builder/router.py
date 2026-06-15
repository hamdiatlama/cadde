from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.website_builder.service import WebsiteBuilderService

router = APIRouter(prefix="/website-builder", tags=["website_builder"])


def get_service(db: AsyncSession = Depends(get_db)) -> WebsiteBuilderService:
    return WebsiteBuilderService(db)


@router.post("/website", status_code=201)
async def create_website(
    hotel_id: int = Query(...),
    domain: str = Query(None),
    subdomain: str = Query(None),
    template_id: str = Query("default"),
    primary_color: str = Query("#4A7FD4"),
    secondary_color: str = Query("#EEF4FF"),
    font_family: str = Query("Space Grotesk"),
    logo_url: str = Query(""),
    hero_image_url: str = Query(""),
    about_text: str = Query(""),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    try:
        result = await svc.create_website(hotel_id, {
            "domain": domain, "subdomain": subdomain,
            "template_id": template_id,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "font_family": font_family,
            "logo_url": logo_url, "hero_image_url": hero_image_url,
            "about_text": about_text,
        })
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/website/{hotel_id}")
async def get_website(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_website(hotel_id)
    if not result:
        raise HTTPException(404, "Website not found")
    return result


@router.put("/website/{hotel_id}")
async def update_website(
    hotel_id: int,
    domain: str = Query(None),
    template_id: str = Query(None),
    primary_color: str = Query(None),
    secondary_color: str = Query(None),
    font_family: str = Query(None),
    logo_url: str = Query(None),
    hero_image_url: str = Query(None),
    about_text: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.update_website(hotel_id, {
        "domain": domain, "template_id": template_id,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "font_family": font_family,
        "logo_url": logo_url, "hero_image_url": hero_image_url,
        "about_text": about_text,
    })
    if not result:
        raise HTTPException(404, "Website not found")
    await db.commit()
    return result


@router.post("/website/{hotel_id}/publish")
async def publish_website(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.publish_website(hotel_id)
    if not result:
        raise HTTPException(404, "Website not found")
    await db.commit()
    return result


@router.get("/pages/{website_id}")
async def list_pages(website_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return await svc.list_pages(website_id)


@router.put("/pages/{page_id}")
async def update_page(
    page_id: int,
    title: str = Query(None),
    content: str = Query(None),
    sort_order: int = Query(None),
    is_active: bool = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.update_page_content(page_id, {
        "title": title, "content": content,
        "sort_order": sort_order, "is_active": is_active,
    })
    if not result:
        raise HTTPException(404, "Page not found")
    await db.commit()
    return result


@router.put("/seo/{seo_id}")
async def update_seo(
    seo_id: int,
    meta_title: str = Query(None),
    meta_description: str = Query(None),
    meta_keywords: str = Query(None),
    og_image_url: str = Query(None),
    canonical_url: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.update_seo(seo_id, {
        "meta_title": meta_title,
        "meta_description": meta_description,
        "meta_keywords": meta_keywords,
        "og_image_url": og_image_url,
        "canonical_url": canonical_url,
    })
    if not result:
        raise HTTPException(404, "SEO not found")
    await db.commit()
    return result


@router.get("/widget/{website_id}")
async def get_booking_widget(website_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_booking_widget(website_id)
    if not result:
        raise HTTPException(404, "Booking widget not found")
    return result


@router.put("/widget/{widget_id}")
async def update_widget(
    widget_id: int,
    widget_type: str = Query(None),
    is_enabled: bool = Query(None),
    embed_code: str = Query(None),
    custom_css: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.update_widget(widget_id, {
        "widget_type": widget_type,
        "is_enabled": is_enabled,
        "embed_code": embed_code,
        "custom_css": custom_css,
    })
    if not result:
        raise HTTPException(404, "Widget not found")
    await db.commit()
    return result


@router.get("/embed/{hotel_id}")
async def get_embed_code(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    site = await svc.repo.get_hotel_website(hotel_id)
    if not site:
        raise HTTPException(404, "Website not found")
    result = await svc.generate_embed_code(hotel_id)
    return result


@router.get("/seo-analysis/{hotel_id}")
async def seo_analysis(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_seo_analysis(hotel_id)
    if not result:
        raise HTTPException(404, "Website not found")
    return result
