from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.auction.repository import AuctionRepository

router = APIRouter(prefix="/auctions", tags=["auctions"])


@router.get("/")
async def list_active_auctions(db: AsyncSession = Depends(get_db)):
    repo = AuctionRepository(db)
    auctions = await repo.list_active()
    return auctions


@router.get("/{auction_id}")
async def get_auction(auction_id: int, db: AsyncSession = Depends(get_db)):
    repo = AuctionRepository(db)
    auction = await repo.get_auction(auction_id)
    if not auction:
        raise HTTPException(404, "Auction not found")
    return auction


@router.post("/", status_code=201)
async def create_auction(
    product_id: int, start_price: float, start_time: datetime, end_time: datetime,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if current_user.role != "seller":
        raise HTTPException(403, "Only sellers can create auctions")
    repo = AuctionRepository(db)
    auction = await repo.create_auction(product_id, start_price, start_time, end_time)
    await db.commit()
    return {"id": auction.id, "product_id": auction.product_id, "status": auction.status}


@router.post("/{auction_id}/bid", status_code=201)
async def place_bid(
    auction_id: int, amount: float,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = AuctionRepository(db)
    try:
        bid = await repo.place_bid(auction_id, current_user.id, amount)
    except ValueError as e:
        raise HTTPException(400, str(e))
    await db.commit()
    return {"id": bid.id, "amount": bid.amount, "bidder_id": bid.bidder_id}


@router.post("/{auction_id}/close")
async def close_auction(
    auction_id: int,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if current_user.role != "seller":
        raise HTTPException(403, "Only sellers can close auctions")
    repo = AuctionRepository(db)
    try:
        auction = await repo.close_auction(auction_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    await db.commit()
    return {"id": auction.id, "winner_id": auction.winner_id, "status": auction.status}
