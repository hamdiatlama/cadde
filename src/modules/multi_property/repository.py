import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.multi_property.models import PropertyGroup, PropertyGroupMember, PropertyGroupInvite, GroupConsolidatedReport


class PropertyGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_groups(self, owner_id: int):
        r = await self.db.execute(
            select(PropertyGroup).where(PropertyGroup.owner_id == owner_id, PropertyGroup.is_active == True)
            .order_by(PropertyGroup.created_at.desc())
        )
        return r.scalars().all()

    async def get_group(self, group_id: int):
        r = await self.db.execute(select(PropertyGroup).where(PropertyGroup.id == group_id))
        return r.scalar_one_or_none()

    async def create_group(self, data: dict) -> PropertyGroup:
        g = PropertyGroup(**data)
        self.db.add(g)
        return g

    async def update_group(self, group_id: int, data: dict):
        r = await self.db.execute(select(PropertyGroup).where(PropertyGroup.id == group_id))
        g = r.scalar_one_or_none()
        if g:
            for k, v in data.items():
                if hasattr(g, k):
                    setattr(g, k, v)
        return g

    async def delete_group(self, group_id: int):
        r = await self.db.execute(select(PropertyGroup).where(PropertyGroup.id == group_id))
        g = r.scalar_one_or_none()
        if g:
            g.is_active = False
        return g

    async def list_group_hotels(self, group_id: int):
        r = await self.db.execute(
            select(PropertyGroupMember).where(PropertyGroupMember.group_id == group_id)
        )
        return r.scalars().all()

    async def add_hotel_to_group(self, group_id: int, hotel_id: int, role: str) -> PropertyGroupMember:
        m = PropertyGroupMember(group_id=group_id, hotel_id=hotel_id, role=role)
        self.db.add(m)
        return m

    async def remove_hotel_from_group(self, group_id: int, hotel_id: int):
        await self.db.execute(
            delete(PropertyGroupMember).where(
                PropertyGroupMember.group_id == group_id,
                PropertyGroupMember.hotel_id == hotel_id
            )
        )

    async def update_member_role(self, member_id: int, role: str):
        r = await self.db.execute(select(PropertyGroupMember).where(PropertyGroupMember.id == member_id))
        m = r.scalar_one_or_none()
        if m:
            m.role = role
        return m

    async def list_invites(self, group_id: int):
        r = await self.db.execute(
            select(PropertyGroupInvite).where(PropertyGroupInvite.group_id == group_id)
            .order_by(PropertyGroupInvite.created_at.desc())
        )
        return r.scalars().all()

    async def create_invite(self, data: dict) -> PropertyGroupInvite:
        data["token"] = str(uuid.uuid4().hex)
        data["expires_at"] = datetime.now(timezone.utc) + timedelta(days=7)
        inv = PropertyGroupInvite(**data)
        self.db.add(inv)
        return inv

    async def accept_invite(self, token: str):
        r = await self.db.execute(select(PropertyGroupInvite).where(PropertyGroupInvite.token == token))
        inv = r.scalar_one_or_none()
        if inv:
            inv.status = "accepted"
        return inv

    async def expire_invite(self, invite_id: int):
        r = await self.db.execute(select(PropertyGroupInvite).where(PropertyGroupInvite.id == invite_id))
        inv = r.scalar_one_or_none()
        if inv:
            inv.status = "expired"
        return inv

    async def get_consolidated_report(self, group_id: int, report_date):
        r = await self.db.execute(
            select(GroupConsolidatedReport).where(
                GroupConsolidatedReport.group_id == group_id,
                GroupConsolidatedReport.report_date == report_date
            )
        )
        return r.scalar_one_or_none()

    async def save_report(self, data: dict) -> GroupConsolidatedReport:
        rpt = GroupConsolidatedReport(**data)
        self.db.add(rpt)
        return rpt
