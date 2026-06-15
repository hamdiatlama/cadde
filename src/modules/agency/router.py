from fastapi import APIRouter, Depends, HTTPException
from src.modules.agency.repository import AgencyRepository, get_agency_repo
from src.modules.agency.service import AgencyService, get_agency_service

router = APIRouter(prefix="/agency", tags=["agency"])


# ─── Agency CRUD ─────────────────────────────────────────────
@router.post("/register")
async def register_agency(user_id: int = 1, data: dict = {},
                           svc: AgencyService = Depends(get_agency_service)):
    try:
        return await svc.register_agency(user_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/my")
async def my_agency(user_id: int = 1,
                     repo: AgencyRepository = Depends(get_agency_repo)):
    agency = await repo.get_agency_by_user(user_id)
    if not agency: raise HTTPException(404, "Acentelik kaydınız bulunamadı")
    return agency


@router.put("/my")
async def update_my_agency(user_id: int = 1, data: dict = {},
                            repo: AgencyRepository = Depends(get_agency_repo)):
    agency = await repo.get_agency_by_user(user_id)
    if not agency: raise HTTPException(404, "Acentelik kaydınız bulunamadı")
    return await repo.update_agency(agency.id, data)


@router.get("/list")
async def list_agencies(is_verified: bool = None, is_active: bool = None,
                         repo: AgencyRepository = Depends(get_agency_repo)):
    return await repo.list_agencies(is_verified, is_active)


@router.get("/{agency_id}")
async def get_agency(agency_id: int,
                      repo: AgencyRepository = Depends(get_agency_repo)):
    a = await repo.get_agency(agency_id)
    if not a: raise HTTPException(404, "Acente bulunamadı")
    return a


# ─── Authorization ───────────────────────────────────────────
@router.post("/authorizations")
async def request_authorization(agency_id: int, domain: str, provider_id: int,
                                  provider_name: str = None, commission_split: float = 0,
                                  svc: AgencyService = Depends(get_agency_service)):
    try:
        return await svc.request_authorization(agency_id, domain, provider_id, provider_name, commission_split)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/authorizations")
async def list_authorizations(agency_id: int = None, domain: str = None,
                                provider_id: int = None, status: str = None,
                                repo: AgencyRepository = Depends(get_agency_repo)):
    return await repo.list_authorizations(agency_id, domain, provider_id, status)


@router.post("/authorizations/{auth_id}/approve")
async def approve_authorization(auth_id: int, authorized_by: int = 1,
                                 repo: AgencyRepository = Depends(get_agency_repo)):
    a = await repo.approve_authorization(auth_id, authorized_by)
    if not a: raise HTTPException(404, "Yetkilendirme bulunamadı")
    return a


@router.post("/authorizations/{auth_id}/reject")
async def reject_authorization(auth_id: int, notes: str = None,
                                repo: AgencyRepository = Depends(get_agency_repo)):
    a = await repo.reject_authorization(auth_id, notes)
    if not a: raise HTTPException(404, "Yetkilendirme bulunamadı")
    return a
