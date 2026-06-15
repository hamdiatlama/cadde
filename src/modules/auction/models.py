from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from src.database import Base


class Auction(Base):
    __tablename__ = "auctions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    start_price = Column(Float, nullable=False)
    current_bid = Column(Float, default=0)
    bidder_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="pending")
    winner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuctionBid(Base):
    __tablename__ = "auction_bids"
    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
