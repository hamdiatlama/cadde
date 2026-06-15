from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class AutomationWorkflow(Base):
    __tablename__ = "automation_workflows"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200))
    trigger_event = Column(String(50))
    conditions = Column(Text)
    actions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorkflowLog(Base):
    __tablename__ = "workflow_logs"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("automation_workflows.id"), nullable=False)
    triggered_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="pending")
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
