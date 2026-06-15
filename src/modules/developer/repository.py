import hashlib
import secrets
from datetime import datetime, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.developer.models import ApiKey, Webhook, WebhookEvent


class ApiKeyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_key(self, seller_id: int, name: str, permissions: str = None) -> tuple:
        raw = "sk_" + secrets.token_hex(24)
        prefix = raw[:10]
        key_hash = hashlib.sha256(raw.encode()).hexdigest()
        ak = ApiKey(seller_id=seller_id, key_hash=key_hash, key_prefix=prefix, name=name, permissions=permissions or "[]")
        self.db.add(ak)
        return raw, ak

    async def list_keys(self, seller_id: int):
        r = await self.db.execute(select(ApiKey).where(ApiKey.seller_id == seller_id, ApiKey.is_active == True))
        return r.scalars().all()

    async def revoke_key(self, key_id: int) -> ApiKey:
        r = await self.db.execute(select(ApiKey).where(ApiKey.id == key_id))
        ak = r.scalar_one_or_none()
        if ak:
            ak.is_active = False
        return ak

    async def validate_key(self, key_hash: str) -> ApiKey:
        r = await self.db.execute(select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.is_active == True))
        ak = r.scalar_one_or_none()
        if ak and ak.expires_at and ak.expires_at < datetime.now(timezone.utc):
            return None
        if ak:
            ak.last_used_at = datetime.now(timezone.utc)
        return ak


class WebhookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, seller_id: int, url: str, events: str = None, secret: str = None) -> Webhook:
        wh = Webhook(seller_id=seller_id, url=url, events=events or "[]", secret=secret)
        self.db.add(wh)
        return wh

    async def list_webhooks(self, seller_id: int):
        r = await self.db.execute(select(Webhook).where(Webhook.seller_id == seller_id, Webhook.is_active == True))
        return r.scalars().all()

    async def delete_webhook(self, webhook_id: int) -> Webhook:
        r = await self.db.execute(select(Webhook).where(Webhook.id == webhook_id))
        wh = r.scalar_one_or_none()
        if wh:
            wh.is_active = False
        return wh

    async def trigger_event(self, webhook_id: int, event_type: str, payload: str) -> WebhookEvent:
        r = await self.db.execute(select(Webhook).where(Webhook.id == webhook_id, Webhook.is_active == True))
        wh = r.scalar_one_or_none()
        if not wh:
            return None
        we = WebhookEvent(webhook_id=webhook_id, event_type=event_type, payload=payload, status="delivering")
        self.db.add(we)
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(wh.url, json={"event": event_type, "payload": payload}, headers={"X-Webhook-Secret": wh.secret or ""})
            we.status = "delivered" if resp.is_success else "failed"
            we.response_code = resp.status_code
            we.response_body = resp.text[:2000]
            wh.last_triggered_at = datetime.now(timezone.utc)
        except Exception as e:
            we.status = "failed"
            we.response_body = str(e)
        return we

    async def list_events(self, webhook_id: int = None, limit: int = 50):
        q = select(WebhookEvent).order_by(WebhookEvent.created_at.desc()).limit(limit)
        if webhook_id:
            q = q.where(WebhookEvent.webhook_id == webhook_id)
        r = await self.db.execute(q)
        return r.scalars().all()
