from datetime import datetime, timezone, date
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.upselling.models import UpsellOffer, UpsellBookingItem, UpsellCampaign, AncillaryRevenueReport


class UpsellOfferRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> UpsellOffer:
        obj = UpsellOffer(**data)
        self.db.add(obj)
        return obj

    async def get(self, offer_id: int) -> UpsellOffer | None:
        r = await self.db.execute(select(UpsellOffer).where(UpsellOffer.id == offer_id))
        return r.scalar_one_or_none()

    async def list_by_hotel(self, hotel_id: int, is_active: bool | None = None) -> list[UpsellOffer]:
        stmt = select(UpsellOffer).where(UpsellOffer.hotel_id == hotel_id)
        if is_active is not None:
            stmt = stmt.where(UpsellOffer.is_active == is_active)
        stmt = stmt.order_by(UpsellOffer.display_order, UpsellOffer.created_at.desc())
        r = await self.db.execute(stmt)
        return list(r.scalars().all())

    async def update(self, offer_id: int, data: dict) -> UpsellOffer | None:
        obj = await self.get(offer_id)
        if not obj:
            return None
        for field, val in data.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj

    async def delete(self, offer_id: int) -> bool:
        obj = await self.get(offer_id)
        if not obj:
            return False
        await self.db.delete(obj)
        return True

    async def list_eligible(self, hotel_id: int, trigger_event: str | None = None) -> list[UpsellOffer]:
        stmt = select(UpsellOffer).where(
            UpsellOffer.hotel_id == hotel_id,
            UpsellOffer.is_active == True,
        )
        if trigger_event:
            stmt = stmt.where(
                (UpsellOffer.trigger_event == trigger_event) | (UpsellOffer.trigger_event.is_(None))
            )
        stmt = stmt.order_by(UpsellOffer.display_order)
        r = await self.db.execute(stmt)
        return list(r.scalars().all())


class UpsellBookingItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> UpsellBookingItem:
        obj = UpsellBookingItem(**data)
        self.db.add(obj)
        return obj

    async def get(self, item_id: int) -> UpsellBookingItem | None:
        r = await self.db.execute(select(UpsellBookingItem).where(UpsellBookingItem.id == item_id))
        return r.scalar_one_or_none()

    async def list_by_booking(self, booking_id: int) -> list[UpsellBookingItem]:
        r = await self.db.execute(
            select(UpsellBookingItem).where(UpsellBookingItem.booking_id == booking_id)
            .order_by(UpsellBookingItem.created_at.desc())
        )
        return list(r.scalars().all())

    async def update_status(self, item_id: int, status: str) -> UpsellBookingItem | None:
        obj = await self.get(item_id)
        if not obj:
            return None
        obj.status = status
        if status == "confirmed":
            obj.confirmed_at = datetime.now(timezone.utc)
        self.db.add(obj)
        return obj

    async def list_by_hotel_and_dates(self, hotel_id: int, date_from: date, date_to: date) -> list[UpsellBookingItem]:
        r = await self.db.execute(
            select(UpsellBookingItem)
            .join(UpsellOffer, UpsellBookingItem.offer_id == UpsellOffer.id)
            .where(
                UpsellOffer.hotel_id == hotel_id,
                UpsellBookingItem.created_at >= date_from,
                UpsellBookingItem.created_at <= date_to,
                UpsellBookingItem.status.in_(["confirmed", "used"]),
            )
        )
        return list(r.scalars().all())


class UpsellCampaignRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> UpsellCampaign:
        obj = UpsellCampaign(**data)
        self.db.add(obj)
        return obj

    async def get(self, campaign_id: int) -> UpsellCampaign | None:
        r = await self.db.execute(select(UpsellCampaign).where(UpsellCampaign.id == campaign_id))
        return r.scalar_one_or_none()

    async def list_by_hotel(self, hotel_id: int, is_active: bool | None = None) -> list[UpsellCampaign]:
        stmt = select(UpsellCampaign).where(UpsellCampaign.hotel_id == hotel_id)
        if is_active is not None:
            stmt = stmt.where(UpsellCampaign.is_active == is_active)
        stmt = stmt.order_by(UpsellCampaign.created_at.desc())
        r = await self.db.execute(stmt)
        return list(r.scalars().all())

    async def update(self, campaign_id: int, data: dict) -> UpsellCampaign | None:
        obj = await self.get(campaign_id)
        if not obj:
            return None
        for field, val in data.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj

    async def delete(self, campaign_id: int) -> bool:
        obj = await self.get(campaign_id)
        if not obj:
            return False
        await self.db.delete(obj)
        return True


class AncillaryReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AncillaryRevenueReport:
        obj = AncillaryRevenueReport(**data)
        self.db.add(obj)
        return obj

    async def get_by_hotel_and_date(self, hotel_id: int, report_date: date) -> AncillaryRevenueReport | None:
        r = await self.db.execute(
            select(AncillaryRevenueReport).where(
                AncillaryRevenueReport.hotel_id == hotel_id,
                AncillaryRevenueReport.report_date == report_date,
            )
        )
        return r.scalar_one_or_none()

    async def list_by_hotel(self, hotel_id: int, limit: int = 30) -> list[AncillaryRevenueReport]:
        r = await self.db.execute(
            select(AncillaryRevenueReport).where(AncillaryRevenueReport.hotel_id == hotel_id)
            .order_by(AncillaryRevenueReport.report_date.desc()).limit(limit)
        )
        return list(r.scalars().all())


class UpsellingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.offers = UpsellOfferRepository(db)
        self.items = UpsellBookingItemRepository(db)
        self.campaigns = UpsellCampaignRepository(db)
        self.reports = AncillaryReportRepository(db)

    async def list_offers(self, hotel_id: int, is_active: bool | None = None) -> list[dict]:
        offers = await self.offers.list_by_hotel(hotel_id, is_active)
        return [
            {
                "id": o.id, "hotel_id": o.hotel_id, "name": o.name,
                "description": o.description, "category": o.category,
                "price": o.price, "currency": o.currency,
                "is_active": o.is_active, "is_auto_offer": o.is_auto_offer,
                "trigger_event": o.trigger_event, "display_order": o.display_order,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in offers
        ]

    async def list_booking_items(self, booking_id: int) -> list[dict]:
        items = await self.items.list_by_booking(booking_id)
        return [
            {
                "id": i.id, "booking_id": i.booking_id, "offer_id": i.offer_id,
                "quantity": i.quantity, "unit_price": i.unit_price,
                "total_price": i.total_price, "status": i.status,
                "added_at": i.added_at.isoformat() if i.added_at else None,
                "confirmed_at": i.confirmed_at.isoformat() if i.confirmed_at else None,
            }
            for i in items
        ]

    async def get_upsell_revenue(self, hotel_id: int, date_from: date, date_to: date) -> dict:
        items = await self.items.list_by_hotel_and_dates(hotel_id, date_from, date_to)
        total = sum(i.total_price or 0 for i in items)
        category_breakdown = {}
        for item in items:
            r = await self.db.execute(select(UpsellOffer).where(UpsellOffer.id == item.offer_id))
            offer = r.scalar_one_or_none()
            cat = offer.category if offer else "unknown"
            category_breakdown[cat] = category_breakdown.get(cat, 0) + (item.total_price or 0)
        return {
            "total_revenue": round(total, 2),
            "total_orders": len(items),
            "breakdown": category_breakdown,
        }
