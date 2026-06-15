from datetime import datetime, timezone, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.upselling.repository import UpsellingRepository
from src.modules.upselling.models import UpsellOffer
from src.modules.hotel.models import Booking


class UpsellingService:
    def __init__(self, db: AsyncSession):
        self.repo = UpsellingRepository(db)
        self.db = db

    async def add_upsell_to_booking(self, booking_id: int, offer_id: int, quantity: int = 1) -> dict:
        r = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = r.scalar_one_or_none()
        if not booking:
            raise ValueError("Booking not found")

        offer = await self.repo.offers.get(offer_id)
        if not offer or not offer.is_active:
            raise ValueError("Offer not found or inactive")

        unit_price = offer.price
        total_price = unit_price * quantity

        item = await self.repo.items.create({
            "booking_id": booking_id,
            "offer_id": offer_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price,
            "status": "pending",
        })
        return {
            "id": item.id, "booking_id": item.booking_id, "offer_id": item.offer_id,
            "quantity": item.quantity, "unit_price": item.unit_price,
            "total_price": item.total_price, "status": item.status,
        }

    async def confirm_upsell_item(self, item_id: int) -> dict:
        item = await self.repo.items.update_status(item_id, "confirmed")
        if not item:
            raise ValueError("Upsell item not found")
        return {
            "id": item.id, "status": item.status,
            "confirmed_at": item.confirmed_at.isoformat() if item.confirmed_at else None,
        }

    async def cancel_upsell_item(self, item_id: int) -> dict:
        item = await self.repo.items.update_status(item_id, "cancelled")
        if not item:
            raise ValueError("Upsell item not found")
        return {"id": item.id, "status": item.status}

    async def get_available_offers(self, booking_id: int, trigger_event: str | None = None) -> list[dict]:
        r = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = r.scalar_one_or_none()
        if not booking:
            raise ValueError("Booking not found")

        offers = await self.repo.offers.list_eligible(booking.hotel_id, trigger_event)
        return [
            {
                "id": o.id, "name": o.name, "description": o.description,
                "category": o.category, "price": o.price, "currency": o.currency,
                "trigger_event": o.trigger_event, "display_order": o.display_order,
            }
            for o in offers
        ]

    async def generate_ancillary_report(self, hotel_id: int, report_date: date) -> dict:
        existing = await self.repo.reports.get_by_hotel_and_date(hotel_id, report_date)
        if existing:
            return {
                "id": existing.id, "hotel_id": existing.hotel_id,
                "report_date": existing.report_date.isoformat() if existing.report_date else None,
                "total_upsell_revenue": existing.total_upsell_revenue,
                "total_orders": existing.total_orders,
                "breakdown": existing.breakdown,
                "created_at": existing.created_at.isoformat() if existing.created_at else None,
            }

        revenue_data = await self.repo.get_upsell_revenue(hotel_id, report_date, report_date)
        report = await self.repo.reports.create({
            "hotel_id": hotel_id,
            "report_date": report_date,
            "total_upsell_revenue": revenue_data["total_revenue"],
            "total_orders": revenue_data["total_orders"],
            "breakdown": revenue_data["breakdown"],
        })
        return {
            "id": report.id, "hotel_id": report.hotel_id,
            "report_date": report.report_date.isoformat() if report.report_date else None,
            "total_upsell_revenue": report.total_upsell_revenue,
            "total_orders": report.total_orders,
            "breakdown": report.breakdown,
            "created_at": report.created_at.isoformat() if report.created_at else None,
        }

    async def create_campaign(self, hotel_id: int, data: dict) -> dict:
        data["hotel_id"] = hotel_id
        campaign = await self.repo.campaigns.create(data)
        return {
            "id": campaign.id, "hotel_id": campaign.hotel_id,
            "name": campaign.name, "description": campaign.description,
            "rules": campaign.rules, "discount_percentage": campaign.discount_percentage,
            "is_active": campaign.is_active,
            "start_date": campaign.start_date.isoformat() if campaign.start_date else None,
            "end_date": campaign.end_date.isoformat() if campaign.end_date else None,
        }
