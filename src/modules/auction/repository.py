from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auction.models import Auction, AuctionBid


class AuctionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_auction(
        self, product_id: int, start_price: float, start_time: datetime, end_time: datetime
    ) -> Auction:
        auction = Auction(
            product_id=product_id,
            start_price=start_price,
            current_bid=start_price,
            start_time=start_time,
            end_time=end_time,
            status="pending",
        )
        self.db.add(auction)
        return auction

    async def place_bid(self, auction_id: int, bidder_id: int, amount: float) -> AuctionBid:
        r = await self.db.execute(select(Auction).where(Auction.id == auction_id))
        auction = r.scalar_one_or_none()
        if not auction:
            raise ValueError("Auction not found")
        if auction.status != "active":
            raise ValueError("Auction is not active")
        if amount <= auction.current_bid:
            raise ValueError("Bid must be higher than current bid")
        auction.current_bid = amount
        auction.bidder_id = bidder_id
        bid = AuctionBid(auction_id=auction_id, bidder_id=bidder_id, amount=amount)
        self.db.add(bid)
        return bid

    async def list_active(self):
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(Auction).where(
                Auction.status == "active",
                Auction.end_time > now
            ).order_by(Auction.end_time.asc())
        )
        return r.scalars().all()

    async def get_auction(self, auction_id: int):
        r = await self.db.execute(select(Auction).where(Auction.id == auction_id))
        return r.scalar_one_or_none()

    async def close_auction(self, auction_id: int):
        r = await self.db.execute(select(Auction).where(Auction.id == auction_id))
        auction = r.scalar_one_or_none()
        if not auction:
            raise ValueError("Auction not found")
        if auction.status != "active":
            raise ValueError("Auction is not active")
        auction.status = "ended"
        if auction.bidder_id:
            auction.winner_id = auction.bidder_id
        return auction
