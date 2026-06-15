from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.ai_concierge.repository import ConciergeRepository
from src.modules.ai_concierge.service import ConciergeService

router = APIRouter(prefix="/ai-concierge", tags=["ai_concierge"])


def get_repo(db: AsyncSession = Depends(get_db)) -> ConciergeRepository:
    return ConciergeRepository(db)


def get_service(db: AsyncSession = Depends(get_db)) -> ConciergeService:
    return ConciergeService(db)


@router.get("/config/{hotel_id}")
async def get_config(hotel_id: int, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    config = await repo.get_config(hotel_id)
    if not config:
        raise HTTPException(404, "Config not found")
    return config


@router.put("/config/{hotel_id}")
async def update_config(hotel_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    config = await repo.update_config(hotel_id, data)
    await db.commit()
    return config


@router.get("/intents/{hotel_id}")
async def list_intents(hotel_id: int, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    return await repo.list_intents(hotel_id)


@router.post("/intents", status_code=201)
async def create_intent(data: dict, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    intent = await repo.create_intent(data)
    await db.commit()
    return intent


@router.put("/intents/{intent_id}")
async def update_intent(intent_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    intent = await repo.update_intent(intent_id, data)
    if not intent:
        raise HTTPException(404, "Intent not found")
    await db.commit()
    return intent


@router.post("/message")
async def process_message(data: dict, db: AsyncSession = Depends(get_db)):
    hotel_id = data.get("hotel_id")
    booking_id = data.get("booking_id")
    message = data.get("message")
    if not all([hotel_id, message]):
        raise HTTPException(400, "hotel_id and message are required")
    repo = get_repo(db)
    conv = await repo.create_conversation({
        "booking_id": booking_id,
        "hotel_id": hotel_id,
        "channel": "in_app",
    })
    await db.flush()
    guest_msg = await repo.add_message(conv.id, {
        "sender_type": "guest",
        "message": message,
    })
    svc = get_service(db)
    response = await svc.generate_auto_response(message, hotel_id, conv.id)
    if response:
        await db.commit()
        return {"conversation_id": conv.id, "response": response, "auto_responded": True}
    config = await repo.get_config(hotel_id)
    threshold = config.escalation_threshold if config else 3
    msgs = await repo.get_messages(conv.id)
    guest_msgs = [m for m in msgs if m.sender_type == "guest"]
    auto_escalate = len(guest_msgs) >= threshold
    if auto_escalate:
        await svc.escalate_to_human(conv.id)
    await db.commit()
    return {
        "conversation_id": conv.id,
        "response": None,
        "auto_responded": False,
        "escalated": auto_escalate,
    }


@router.post("/escalate/{conversation_id}")
async def escalate_conversation(conversation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    conv = await svc.escalate_to_human(conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    await db.commit()
    return conv


@router.get("/conversations/{hotel_id}")
async def list_conversations(hotel_id: int, status: str = None, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    convs = await repo.list_conversations(hotel_id, status)
    result = []
    for conv in convs:
        msgs = await repo.get_messages(conv.id)
        result.append({
            "id": conv.id,
            "booking_id": conv.booking_id,
            "guest_id": conv.guest_id,
            "hotel_id": conv.hotel_id,
            "channel": conv.channel,
            "status": conv.status,
            "started_at": conv.started_at.isoformat() if conv.started_at else None,
            "resolved_at": conv.resolved_at.isoformat() if conv.resolved_at else None,
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "messages": [
                {
                    "id": m.id,
                    "sender_type": m.sender_type,
                    "message": m.message,
                    "intent_matched": m.intent_matched,
                    "is_auto_response": m.is_auto_response,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in msgs
            ],
        })
    return result


@router.get("/knowledge-base/{hotel_id}")
async def list_kb_entries(hotel_id: int, category: str = None, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    return await repo.list_kb_entries(hotel_id, category)


@router.post("/knowledge-base", status_code=201)
async def create_kb_entry(data: dict, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    entry = await repo.create_kb_entry(data)
    await db.commit()
    return entry


@router.get("/sequences/{hotel_id}")
async def list_sequences(hotel_id: int, trigger_event: str = None, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    return await repo.list_sequences(hotel_id, trigger_event)


@router.post("/sequences", status_code=201)
async def create_sequence(data: dict, db: AsyncSession = Depends(get_db)):
    repo = get_repo(db)
    seq = await repo.create_sequence(data)
    await db.commit()
    return seq


@router.post("/trigger/{booking_id}/{event}")
async def trigger_sequence(booking_id: int, event: str, hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.trigger_sequence(hotel_id, booking_id, event)
    await db.commit()
    return results


@router.get("/analytics/{hotel_id}")
async def get_analytics(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return await svc.get_concierge_analytics(hotel_id)
