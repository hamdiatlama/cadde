from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.b2b.models import B2bPriceTier, B2bCustomer, B2bQuote, B2bQuoteItem


class B2bRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_price_tier(self, product_id: int, qty: int):
        r = await self.db.execute(
            select(B2bPriceTier).where(
                B2bPriceTier.product_id == product_id, B2bPriceTier.min_qty <= qty,
                B2bPriceTier.is_active == True
            ).order_by(B2bPriceTier.min_qty.desc()).limit(1)
        )
        return r.scalar_one_or_none()

    async def list_price_tiers(self, product_id: int):
        r = await self.db.execute(
            select(B2bPriceTier).where(B2bPriceTier.product_id == product_id, B2bPriceTier.is_active == True)
            .order_by(B2bPriceTier.min_qty)
        )
        return r.scalars().all()

    async def create_price_tier(self, product_id: int, min_qty: int, unit_price: float, max_qty: int = None) -> B2bPriceTier:
        t = B2bPriceTier(product_id=product_id, min_qty=min_qty, max_qty=max_qty, unit_price=unit_price)
        self.db.add(t); return t

    async def get_or_create_customer(self, user_id: int, company_name: str = None, tax_office: str = None, tax_number: str = None) -> B2bCustomer:
        r = await self.db.execute(select(B2bCustomer).where(B2bCustomer.user_id == user_id))
        c = r.scalar_one_or_none()
        if not c:
            c = B2bCustomer(user_id=user_id, company_name=company_name, tax_office=tax_office, tax_number=tax_number)
            self.db.add(c)
        return c

    async def create_quote(self, customer_id: int, seller_id: int, notes: str = None) -> B2bQuote:
        q = B2bQuote(customer_id=customer_id, seller_id=seller_id, notes=notes)
        self.db.add(q); return q

    async def add_quote_item(self, quote_id: int, product_id: int, quantity: int, unit_price: float) -> B2bQuoteItem:
        i = B2bQuoteItem(quote_id=quote_id, product_id=product_id, quantity=quantity, unit_price=unit_price)
        self.db.add(i); return i

    async def list_quotes(self, seller_id: int = None, customer_id: int = None):
        q = select(B2bQuote)
        if seller_id: q = q.where(B2bQuote.seller_id == seller_id)
        if customer_id: q = q.where(B2bQuote.customer_id == customer_id)
        q = q.order_by(B2bQuote.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()
