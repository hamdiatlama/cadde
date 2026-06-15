from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.trade_in.models import TradeInRequest, RefurbishedProduct


class TradeInRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_trade_in_request(self, user_id: int, product_to_trade: str, condition: str, estimated_value: float = None, target_product_id: int = None) -> TradeInRequest:
        r = TradeInRequest(user_id=user_id, product_to_trade=product_to_trade, condition=condition, estimated_value=estimated_value, target_product_id=target_product_id)
        self.db.add(r)
        return r

    async def list_requests(self, user_id: int):
        r = await self.db.execute(
            select(TradeInRequest).where(TradeInRequest.user_id == user_id).order_by(TradeInRequest.created_at.desc())
        )
        return r.scalars().all()

    async def create_refurbished_product(self, seller_id: int, original_product_id: int, condition_grade: str, price: float, stock: int = 1) -> RefurbishedProduct:
        rp = RefurbishedProduct(seller_id=seller_id, original_product_id=original_product_id, condition_grade=condition_grade, price=price, stock=stock)
        self.db.add(rp)
        return rp

    async def list_refurbished(self):
        r = await self.db.execute(
            select(RefurbishedProduct).where(RefurbishedProduct.is_active == True).order_by(RefurbishedProduct.created_at.desc())
        )
        return r.scalars().all()
