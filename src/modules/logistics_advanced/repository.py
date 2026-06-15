import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.logistics_advanced.models import Carrier, CarrierRate, Shipment, CarbonFootprint, GiftWrap


class CarrierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_carrier(self, **kwargs) -> Carrier:
        c = Carrier(**kwargs)
        self.db.add(c)
        return c

    async def add_rate(self, carrier_id: int, **kwargs) -> CarrierRate:
        r = CarrierRate(carrier_id=carrier_id, **kwargs)
        self.db.add(r)
        return r

    async def get_rates(self, weight: float) -> list[dict]:
        r = await self.db.execute(
            select(CarrierRate).where(
                CarrierRate.weight_min <= weight,
                (CarrierRate.weight_max == None) | (CarrierRate.weight_max >= weight),
            ).order_by(CarrierRate.price)
        )
        rates = r.scalars().all()
        result = []
        for rate in rates:
            cr = await self.db.execute(select(Carrier).where(Carrier.id == rate.carrier_id))
            carrier = cr.scalar_one_or_none()
            if carrier and carrier.is_active:
                result.append({
                    "carrier_id": carrier.id,
                    "carrier_name": carrier.name,
                    "service_name": rate.service_name,
                    "price": rate.price,
                    "estimated_days_min": rate.estimated_days_min,
                    "estimated_days_max": rate.estimated_days_max,
                })
        return result

    async def list_carriers(self) -> list[Carrier]:
        r = await self.db.execute(select(Carrier).where(Carrier.is_active == True))
        return list(r.scalars().all())


class ShipmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_shipment(self, order_id: int, carrier_id: int, service: str, **kwargs) -> Shipment:
        s = Shipment(order_id=order_id, carrier_id=carrier_id, service_name=service, **kwargs)
        self.db.add(s)
        return s

    async def generate_label(self, shipment_id: int) -> Shipment | None:
        r = await self.db.execute(select(Shipment).where(Shipment.id == shipment_id))
        s = r.scalar_one_or_none()
        if s:
            s.label_url = f"https://labels.example.com/{shipment_id}.pdf"
            s.status = "labeled"
        return s

    async def update_tracking(self, shipment_id: int, tracking_no: str, status: str = None) -> Shipment | None:
        r = await self.db.execute(select(Shipment).where(Shipment.id == shipment_id))
        s = r.scalar_one_or_none()
        if s:
            s.tracking_no = tracking_no
            if status:
                s.status = status
        return s

    async def rate_shopping(self, order_weight: float) -> list[dict]:
        repo = CarrierRepository(self.db)
        return await repo.get_rates(order_weight)

    async def get_by_id(self, shipment_id: int) -> Shipment | None:
        r = await self.db.execute(select(Shipment).where(Shipment.id == shipment_id))
        return r.scalar_one_or_none()

    async def get_by_tracking(self, tracking_no: str) -> Shipment | None:
        r = await self.db.execute(select(Shipment).where(Shipment.tracking_no == tracking_no))
        return r.scalar_one_or_none()


class CarbonFootprintRepository:
    CO2_PER_KG_KM = 0.00015

    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate(self, order_id: int, weight: float, distance: float) -> CarbonFootprint:
        co2_grams = weight * distance * self.CO2_PER_KG_KM * 1000
        offset_cost = co2_grams * 0.00002
        cf = CarbonFootprint(order_id=order_id, co2_grams=round(co2_grams, 2), offset_cost=round(offset_cost, 4))
        self.db.add(cf)
        return cf

    async def create_offset(self, order_id: int) -> CarbonFootprint | None:
        r = await self.db.execute(
            select(CarbonFootprint).where(CarbonFootprint.order_id == order_id, CarbonFootprint.offset_paid == False)
        )
        cf = r.scalar_one_or_none()
        if cf:
            cf.offset_paid = True
        return cf

    async def get_total(self, seller_id: int) -> dict:
        from sqlalchemy import func
        r = await self.db.execute(
            select(
                func.coalesce(func.sum(CarbonFootprint.co2_grams), 0),
                func.coalesce(func.sum(CarbonFootprint.offset_cost), 0),
                func.count(CarbonFootprint.id),
            )
        )
        total_co2, total_cost, count = r.one()
        return {"total_co2_grams": float(total_co2), "total_offset_cost": float(total_cost), "offsets_count": count}


class GiftWrapRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_option(self, seller_id: int, **kwargs) -> GiftWrap:
        gw = GiftWrap(seller_id=seller_id, **kwargs)
        self.db.add(gw)
        return gw

    async def list_options(self, seller_id: int) -> list[GiftWrap]:
        r = await self.db.execute(
            select(GiftWrap).where(GiftWrap.seller_id == seller_id, GiftWrap.is_active == True)
        )
        return list(r.scalars().all())
