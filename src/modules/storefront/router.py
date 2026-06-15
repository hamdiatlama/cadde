from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.storefront.repository import PwaManifestRepository, CookieConsentRepository, GdprRepository

router = APIRouter(prefix="/storefront", tags=["storefront"])


@router.post("/pwa/manifest")
async def create_or_update_pwa_manifest(
    name: str = None, short_name: str = None, icon_url: str = None,
    theme_color: str = None, background_color: str = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = PwaManifestRepository(db)
    data = {k: v for k, v in {"name": name, "short_name": short_name, "icon_url": icon_url,
                               "theme_color": theme_color, "background_color": background_color}.items() if v is not None}
    manifest = await repo.create_or_update_manifest(current_user.id, data)
    await db.commit()
    return manifest


@router.get("/pwa/manifest")
async def get_pwa_manifest(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = PwaManifestRepository(db)
    manifest = await repo.get_manifest(current_user.id)
    if not manifest:
        raise HTTPException(404, "Manifest not found")
    return manifest


@router.post("/cookie-consent", status_code=201)
async def record_cookie_consent(
    consent_type: str, session_id: str = None, ip_address: str = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = CookieConsentRepository(db)
    consent = await repo.record_consent(current_user.id, consent_type, session_id, ip_address)
    await db.commit()
    return consent


@router.get("/cookie-consent")
async def get_cookie_consent(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = CookieConsentRepository(db)
    return await repo.get_user_consent(current_user.id)


@router.post("/gdpr/request", status_code=201)
async def create_gdpr_request(
    request_type: str,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if request_type not in ("export", "delete", "rectify"):
        raise HTTPException(400, "Invalid request type")
    repo = GdprRepository(db)
    req = await repo.create_request(current_user.id, request_type)
    await db.commit()
    return req


@router.get("/gdpr/requests/my")
async def get_my_gdpr_requests(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select
    from src.modules.storefront.models import GdprDataRequest
    r = await db.execute(
        select(GdprDataRequest).where(GdprDataRequest.user_id == current_user.id)
        .order_by(GdprDataRequest.created_at.desc())
    )
    return r.scalars().all()


@router.get("/gdpr/export")
async def export_my_data(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = GdprRepository(db)
    data = await repo.export_data(current_user.id)
    return data
