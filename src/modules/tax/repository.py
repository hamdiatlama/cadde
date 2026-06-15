from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.tax.models import TaxRate, Invoice


class TaxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tax_rate(self, category_id: int = None):
        q = select(TaxRate).where(TaxRate.is_active == True)
        if category_id:
            q = q.where(TaxRate.category_id == category_id)
        q = q.order_by(TaxRate.category_id.desc().nullslast()).limit(1)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()

    async def get_default_tax_rate(self):
        r = await self.db.execute(select(TaxRate).where(TaxRate.is_active == True, TaxRate.category_id == None).limit(1))
        return r.scalar_one_or_none()

    async def create_tax_rate(self, rate: float, tax_type: str = "kdv", category_id: int = None) -> TaxRate:
        t = TaxRate(rate=rate, tax_type=tax_type, category_id=category_id)
        self.db.add(t); return t

    async def create_invoice(self, order_id: int, invoice_no: str, buyer_id: int, seller_id: int,
                              subtotal: float, tax_total: float, grand_total: float) -> Invoice:
        inv = Invoice(order_id=order_id, invoice_no=invoice_no, buyer_id=buyer_id, seller_id=seller_id,
                       subtotal=subtotal, tax_total=tax_total, grand_total=grand_total)
        self.db.add(inv); return inv

    async def list_invoices(self, user_id: int, as_buyer: bool = True):
        q = select(Invoice).where(
            Invoice.buyer_id == user_id if as_buyer else Invoice.seller_id == user_id
        ).order_by(Invoice.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()


class TaxService:
    def __init__(self, db):
        self.repo = TaxRepository(db)

    async def calculate_tax(self, subtotal: float, category_id: int = None) -> dict:
        rate = await self.repo.get_tax_rate(category_id)
        if not rate:
            rate = await self.repo.get_default_tax_rate()
        tax_rate = rate.rate if rate else 20.0
        tax_total = round(subtotal * tax_rate / 100, 2)
        return {"rate": tax_rate, "tax_total": tax_total, "grand_total": round(subtotal + tax_total, 2)}

    async def generate_invoice_no(self) -> str:
        import random
        return f"INV-{random.randint(100000, 999999)}"
