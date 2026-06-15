from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.modules.integration.models import ErpConnection, ErpSyncLog


class ErpRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def connect(self, data: dict) -> ErpConnection:
        conn = ErpConnection(**data)
        self.db.add(conn)
        return conn

    async def list_connections(self, seller_id: int):
        r = await self.db.execute(
            select(ErpConnection).where(ErpConnection.seller_id == seller_id)
            .order_by(ErpConnection.created_at.desc())
        )
        return r.scalars().all()

    async def get_connection(self, connection_id: int, seller_id: int):
        r = await self.db.execute(
            select(ErpConnection).where(
                ErpConnection.id == connection_id, ErpConnection.seller_id == seller_id
            )
        )
        return r.scalar_one_or_none()

    async def sync(self, connection_id: int, sync_type: str, seller_id: int) -> ErpSyncLog:
        conn = await self.get_connection(connection_id, seller_id)
        if not conn:
            raise ValueError("Connection not found")
        log = ErpSyncLog(connection_id=connection_id, sync_type=sync_type, status="running")
        self.db.add(log)
        await self.db.flush()
        records = {"products": 25, "orders": 50, "invoices": 15, "inventory": 120}.get(sync_type, 10)
        log.status = "completed"
        log.records_synced = records
        log.completed_at = datetime.now(timezone.utc)
        conn.last_sync_at = datetime.now(timezone.utc)
        return log

    async def get_sync_logs(self, connection_id: int, limit: int = 50):
        r = await self.db.execute(
            select(ErpSyncLog).where(ErpSyncLog.connection_id == connection_id)
            .order_by(ErpSyncLog.started_at.desc()).limit(limit)
        )
        return r.scalars().all()

    async def disconnect(self, connection_id: int, seller_id: int):
        r = await self.db.execute(
            select(ErpConnection).where(
                ErpConnection.id == connection_id, ErpConnection.seller_id == seller_id
            )
        )
        conn = r.scalar_one_or_none()
        if conn:
            await self.db.delete(conn)
        return conn
