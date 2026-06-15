import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.tax_extended.models import TaxRateAddress, GibInvoice, InternationalDocument


class TaxRateAddressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def set_rate(self, country: str, rate: float, state: str = None, city: str = None, tax_type: str = "vat") -> TaxRateAddress:
        r = TaxRateAddress(country=country, state=state, city=city, rate=rate, tax_type=tax_type)
        self.db.add(r)
        return r

    async def get_rate(self, country: str, state: str = None, city: str = None):
        q = select(TaxRateAddress).where(
            TaxRateAddress.country == country, TaxRateAddress.is_active == True
        )
        if city:
            q = q.where(TaxRateAddress.city == city)
        elif state:
            q = q.where(TaxRateAddress.state == state)
        q = q.order_by(TaxRateAddress.created_at.desc()).limit(1)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()

    async def list_rates(self):
        r = await self.db.execute(select(TaxRateAddress).order_by(TaxRateAddress.country, TaxRateAddress.state))
        return r.scalars().all()


class GibInvoiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invoice(self, order_id: int) -> GibInvoice:
        inv = GibInvoice(
            order_id=order_id,
            invoice_no=f"INV-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}",
        )
        self.db.add(inv)
        return inv

    async def update_gib_status(self, invoice_id: int, status: str, gib_id: str = None, xml_content: str = None, qr_code: str = None) -> GibInvoice:
        r = await self.db.execute(select(GibInvoice).where(GibInvoice.id == invoice_id))
        inv = r.scalar_one_or_none()
        if inv:
            inv.status = status
            if gib_id:
                inv.gib_id = gib_id
            if xml_content:
                inv.xml_content = xml_content
            if qr_code:
                inv.qr_code = qr_code
        return inv

    async def get_by_order(self, order_id: int):
        r = await self.db.execute(
            select(GibInvoice).where(GibInvoice.order_id == order_id)
            .order_by(GibInvoice.created_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()


class InternationalDocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_doc(self, order_id: int, doc_type: str) -> InternationalDocument:
        doc = InternationalDocument(
            order_id=order_id, doc_type=doc_type,
            doc_number=f"{doc_type.upper()}-{uuid.uuid4().hex[:12].upper()}",
            file_url=f"/documents/{order_id}/{doc_type}.pdf",
        )
        self.db.add(doc)
        return doc

    async def list_by_order(self, order_id: int):
        r = await self.db.execute(
            select(InternationalDocument).where(InternationalDocument.order_id == order_id)
            .order_by(InternationalDocument.created_at.desc())
        )
        return r.scalars().all()
