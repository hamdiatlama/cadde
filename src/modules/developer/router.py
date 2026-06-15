from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.developer.repository import ApiKeyRepository, WebhookRepository

router = APIRouter(prefix="/developer", tags=["developer"])


@router.post("/api-keys", status_code=201)
async def generate_api_key(name: str, permissions: str = None,
                           current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ApiKeyRepository(db)
    raw, ak = await repo.generate_key(current_user.id, name, permissions)
    await db.commit()
    return {"id": ak.id, "key": raw, "prefix": ak.key_prefix, "name": ak.name}


@router.get("/api-keys")
async def list_api_keys(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ApiKeyRepository(db)
    keys = await repo.list_keys(current_user.id)
    return [{"id": k.id, "prefix": k.key_prefix, "name": k.name, "permissions": k.permissions, "created_at": k.created_at} for k in keys]


@router.delete("/api-keys/{key_id}")
async def revoke_api_key(key_id: int,
                         current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ApiKeyRepository(db)
    ak = await repo.revoke_key(key_id)
    if not ak:
        raise HTTPException(404, "API key not found")
    await db.commit()
    return {"id": ak.id, "is_active": ak.is_active}


@router.post("/webhooks", status_code=201)
async def register_webhook(url: str, events: str = None, secret: str = None,
                           current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WebhookRepository(db)
    wh = await repo.register(current_user.id, url, events, secret)
    await db.commit()
    return {"id": wh.id, "url": wh.url}


@router.get("/webhooks")
async def list_webhooks(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WebhookRepository(db)
    return await repo.list_webhooks(current_user.id)


@router.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: int,
                         current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WebhookRepository(db)
    wh = await repo.delete_webhook(webhook_id)
    if not wh:
        raise HTTPException(404, "Webhook not found")
    await db.commit()
    return {"id": wh.id, "is_active": wh.is_active}


@router.get("/webhooks/events")
async def list_webhook_events(webhook_id: int = None, limit: int = 50,
                              current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WebhookRepository(db)
    return await repo.list_events(webhook_id, limit)


@router.post("/webhooks/{webhook_id}/test")
async def test_webhook(webhook_id: int,
                       current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = WebhookRepository(db)
    we = await repo.trigger_event(webhook_id, "test", '{"test": true}')
    if not we:
        raise HTTPException(404, "Webhook not found")
    await db.commit()
    return {"id": we.id, "status": we.status, "response_code": we.response_code}
