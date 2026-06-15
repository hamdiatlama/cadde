import json
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.marketing_automation.models import AutomationWorkflow, WorkflowLog

class MarketingAutomationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workflow(self, seller_id: int, name: str, trigger_event: str, conditions: dict, actions: dict) -> AutomationWorkflow:
        wf = AutomationWorkflow(
            seller_id=seller_id, name=name, trigger_event=trigger_event,
            conditions=json.dumps(conditions), actions=json.dumps(actions),
        )
        self.db.add(wf)
        return wf

    async def list_workflows(self, seller_id: int) -> list[AutomationWorkflow]:
        r = await self.db.execute(
            select(AutomationWorkflow).where(AutomationWorkflow.seller_id == seller_id)
            .order_by(AutomationWorkflow.created_at.desc())
        )
        return r.scalars().all()

    async def toggle_workflow(self, workflow_id: int) -> AutomationWorkflow | None:
        r = await self.db.execute(
            select(AutomationWorkflow).where(AutomationWorkflow.id == workflow_id)
        )
        wf = r.scalar_one_or_none()
        if wf:
            wf.is_active = not wf.is_active
        return wf

    async def trigger(self, workflow_id: int, user_id: int) -> WorkflowLog:
        r = await self.db.execute(
            select(AutomationWorkflow).where(AutomationWorkflow.id == workflow_id)
        )
        wf = r.scalar_one_or_none()
        if not wf:
            raise ValueError("Workflow not found")
        log = WorkflowLog(workflow_id=workflow_id, triggered_by=user_id, status="completed")
        actions = json.loads(wf.actions) if isinstance(wf.actions, str) else wf.actions
        log.result = json.dumps({"action": actions.get("action"), "status": "simulated"})
        self.db.add(log)
        return log

    async def get_logs(self, workflow_id: int) -> list[WorkflowLog]:
        r = await self.db.execute(
            select(WorkflowLog).where(WorkflowLog.workflow_id == workflow_id)
            .order_by(WorkflowLog.created_at.desc())
        )
        return r.scalars().all()
