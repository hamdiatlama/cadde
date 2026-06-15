from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.multi_property.repository import PropertyGroupRepository
from src.modules.multi_property.service import PropertyGroupService

router = APIRouter(prefix="/multi-property", tags=["multi_property"])


@router.post("/groups", status_code=201)
async def create_group(
    name: str, description: str = None, logo_url: str = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    svc = PropertyGroupService(db)
    group = await svc.create_group(current_user.id, name, description, logo_url)
    await db.commit()
    return {"id": group.id, "name": group.name}


@router.get("/groups")
async def list_groups(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = PropertyGroupRepository(db)
    return await repo.list_groups(current_user.id)


@router.get("/groups/{group_id}")
async def get_group(
    group_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = PropertyGroupRepository(db)
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    members = await repo.list_group_hotels(group_id)
    invites = await repo.list_invites(group_id)
    return {
        "group": group,
        "members": members,
        "invites": invites,
    }


@router.put("/groups/{group_id}")
async def update_group(
    group_id: int, name: str = None, description: str = None, logo_url: str = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = PropertyGroupRepository(db)
    data = {}
    if name is not None: data["name"] = name
    if description is not None: data["description"] = description
    if logo_url is not None: data["logo_url"] = logo_url
    group = await repo.update_group(group_id, data)
    if not group:
        raise HTTPException(404, "Group not found")
    await db.commit()
    return group


@router.delete("/groups/{group_id}")
async def delete_group(
    group_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = PropertyGroupRepository(db)
    group = await repo.delete_group(group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    await db.commit()
    return {"detail": "Group deleted"}


@router.post("/groups/{group_id}/hotels", status_code=201)
async def add_hotel_to_group(
    group_id: int, hotel_id: int, role: str = "staff",
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = PropertyGroupRepository(db)
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    member = await repo.add_hotel_to_group(group_id, hotel_id, role)
    await db.commit()
    return member


@router.delete("/groups/{group_id}/hotels/{hotel_id}")
async def remove_hotel_from_group(
    group_id: int, hotel_id: int,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = PropertyGroupRepository(db)
    await repo.remove_hotel_from_group(group_id, hotel_id)
    await db.commit()
    return {"detail": "Hotel removed from group"}


@router.post("/groups/{group_id}/invite", status_code=201)
async def invite_member(
    group_id: int, email: str, role: str = "staff",
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    svc = PropertyGroupService(db)
    invite = await svc.invite_member(group_id, email, role, current_user.id)
    await db.commit()
    return {"token": invite.token, "email": invite.email, "role": invite.role}


@router.post("/invite/{token}/accept")
async def accept_invite(
    token: str, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    svc = PropertyGroupService(db)
    invite = await svc.accept_group_invite(token, current_user.id)
    if not invite:
        raise HTTPException(404, "Invite not found")
    if invite.status == "expired":
        raise HTTPException(400, "Invite expired")
    await db.commit()
    return {"detail": "Invite accepted", "group_id": invite.group_id}


@router.get("/groups/{group_id}/dashboard")
async def group_dashboard(
    group_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    svc = PropertyGroupService(db)
    return await svc.get_group_dashboard(group_id)


@router.post("/groups/{group_id}/report")
async def generate_report(
    group_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    svc = PropertyGroupService(db)
    report = await svc.generate_consolidated_report(group_id)
    await db.commit()
    return report
