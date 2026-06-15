from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class ErpConnection(Base):
    __tablename__ = "erp_connections"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    erp_type = Column(String(50))
    api_url = Column(String(500))
    api_key = Column(Text)
    api_secret = Column(Text)
    company_id = Column(String(100))
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ErpSyncLog(Base):
    __tablename__ = "erp_sync_logs"
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("erp_connections.id"), nullable=False)
    sync_type = Column(String(50))
    status = Column(String(20), default="pending")
    records_synced = Column(Integer, default=0)
    error = Column(Text)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
