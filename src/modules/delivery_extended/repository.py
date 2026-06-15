from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.delivery_extended.models import DeliverySlot, ExpressDelivery, PickupPoint, InternationalShipment


class DeliveryExtendedRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_slot(self, seller_id: int, date: str, start_time: str, end_time: str,
                          max_orders: int = 10) -> DeliverySlot:
        s = DeliverySlot(seller_id=seller_id, date=date, start_time=start_time,
                         end_time=end_time, max_orders=max_orders)
        self.db.add(s); return s

    async def list_available_slots(self, date: str):
        r = await self.db.execute(
            select(DeliverySlot).where(DeliverySlot.date == date, DeliverySlot.is_active == True,
                                       DeliverySlot.current_orders < DeliverySlot.max_orders)
            .order_by(DeliverySlot.start_time)
        )
        return r.scalars().all()

    async def book_slot(self, slot_id: int) -> DeliverySlot:
        r = await self.db.execute(select(DeliverySlot).where(DeliverySlot.id == slot_id))
        s = r.scalar_one_or_none()
        if s and s.current_orders < s.max_orders:
            s.current_orders += 1
        return s

    async def create_express(self, order_id: int, fee: float) -> ExpressDelivery:
        e = ExpressDelivery(order_id=order_id, fee=fee)
        self.db.add(e); return e

    async def assign_courier(self, express_id: int, courier_id: int) -> ExpressDelivery:
        r = await self.db.execute(select(ExpressDelivery).where(ExpressDelivery.id == express_id))
        e = r.scalar_one_or_none()
        if e:
            e.courier_id = courier_id
            e.status = "assigned"
        return e

    async def create_pickup_point(self, name: str, address: str, city: str,
                                  lat: float = None, lng: float = None) -> PickupPoint:
        p = PickupPoint(name=name, address=address, city=city, lat=lat, lng=lng)
        self.db.add(p); return p

    async def list_pickup_points(self, city: str = None):
        q = select(PickupPoint).where(PickupPoint.is_active == True)
        if city:
            q = q.where(PickupPoint.city == city)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def create_international_shipment(self, order_id: int, origin_country: str,
                                            destination_country: str, customs_value: float = None,
                                            shipping_cost: float = None) -> InternationalShipment:
        s = InternationalShipment(order_id=order_id, origin_country=origin_country,
                                  destination_country=destination_country,
                                  customs_value=customs_value, shipping_cost=shipping_cost)
        self.db.add(s); return s

    async def get_shipment(self, shipment_id: int) -> InternationalShipment:
        r = await self.db.execute(select(InternationalShipment).where(InternationalShipment.id == shipment_id))
        return r.scalar_one_or_none()
