from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.agency.models import Agency, AgencyAuthorization
from fastapi import Depends


class AgencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── Agency ─────────────────────────────────────────
    async def create_agency(self, data: dict):
        a = Agency(**data)
        self.db.add(a); await self.db.commit(); await self.db.refresh(a)
        return a

    async def get_agency(self, agency_id: int):
        r = await self.db.execute(select(Agency).where(Agency.id == agency_id))
        return r.scalar_one_or_none()

    async def get_agency_by_user(self, user_id: int):
        r = await self.db.execute(select(Agency).where(Agency.user_id == user_id))
        return r.scalar_one_or_none()

    async def list_agencies(self, is_verified: bool = None, is_active: bool = None):
        q = select(Agency)
        if is_verified is not None: q = q.where(Agency.is_verified == is_verified)
        if is_active is not None: q = q.where(Agency.is_active == is_active)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_agency(self, agency_id: int, data: dict):
        r = await self.db.execute(select(Agency).where(Agency.id == agency_id))
        a = r.scalar_one_or_none()
        if a:
            for k, v in data.items():
                setattr(a, k, v)
            await self.db.commit(); await self.db.refresh(a)
        return a

    # ─── Authorization ──────────────────────────────────
    async def create_authorization(self, data: dict):
        a = AgencyAuthorization(**data)
        self.db.add(a); await self.db.commit(); await self.db.refresh(a)
        return a

    async def get_authorization(self, auth_id: int):
        r = await self.db.execute(select(AgencyAuthorization).where(AgencyAuthorization.id == auth_id))
        return r.scalar_one_or_none()

    async def list_authorizations(self, agency_id: int = None, domain: str = None,
                                   provider_id: int = None, status: str = None):
        q = select(AgencyAuthorization)
        if agency_id: q = q.where(AgencyAuthorization.agency_id == agency_id)
        if domain: q = q.where(AgencyAuthorization.domain == domain)
        if provider_id: q = q.where(AgencyAuthorization.provider_id == provider_id)
        if status: q = q.where(AgencyAuthorization.status == status)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def approve_authorization(self, auth_id: int, authorized_by: int):
        r = await self.db.execute(select(AgencyAuthorization).where(AgencyAuthorization.id == auth_id))
        a = r.scalar_one_or_none()
        if a:
            a.status = "approved"
            a.authorized_by = authorized_by
            a.authorized_at = func.now()
            await self.db.commit(); await self.db.refresh(a)
        return a

    async def reject_authorization(self, auth_id: int, notes: str = None):
        r = await self.db.execute(select(AgencyAuthorization).where(AgencyAuthorization.id == auth_id))
        a = r.scalar_one_or_none()
        if a:
            a.status = "rejected"
            if notes: a.notes = notes
            await self.db.commit(); await self.db.refresh(a)
        return a


def get_agency_repo(db: AsyncSession = Depends(get_db)) -> AgencyRepository:
    return AgencyRepository(db)
