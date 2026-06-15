from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, UniqueConstraint
from src.database import Base


class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), default="Favorilerim")
    is_public = Column(Boolean, default=False)
    share_code = Column(String(32), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("wishlist_id", "product_id"),)
