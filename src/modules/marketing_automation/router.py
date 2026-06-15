from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.marketing_automation.repository import MarketingAutomationRepository

router = APIRouter(prefix="/marketing-automation", tags=["marketing_automation"])

@router.post("/workflows", status_code=201)
async def create_workflow(
    name: str, trigger_event: str, conditions: dict, actions: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MarketingAutomationRepository(db)
    wf = await repo.create_workflow(current_user.id, name, trigger_event, conditions, actions)
    await db.commit()
    return wf

@router.get("/workflows")
async def list_workflows(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MarketingAutomationRepository(db)
    return await repo.list_workflows(current_user.id)

@router.put("/workflows/{wf_id}/toggle")
async def toggle_workflow(
    wf_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MarketingAutomationRepository(db)
    wf = await repo.toggle_workflow(wf_id)
    if not wf:
        raise HTTPException(404, "Workflow not found")
    await db.commit()
    return wf

@router.post("/workflows/{wf_id}/test")
async def test_trigger(
    wf_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MarketingAutomationRepository(db)
    try:
        log = await repo.trigger(wf_id, current_user.id)
        await db.commit()
        return log
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.get("/workflows/{wf_id}/logs")
async def get_logs(
    wf_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = MarketingAutomationRepository(db)
    return await repo.get_logs(wf_id)
