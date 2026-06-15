from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.cargo.models import (
    CargoCompany, CargoBranch, CargoCourier, CargoShipment,
    CargoTracking, CargoPricingTier, CargoServiceArea, CargoSellerAgreement,
    CargoProductShipping, CargoDeliverySurvey, CargoReturnRequest,
)


class CompanyRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoCompany:
        obj = CargoCompany(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoCompany, **kwargs) -> CargoCompany:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, company_id: int) -> CargoCompany | None:
        r = await self.db.execute(select(CargoCompany).where(CargoCompany.id == company_id))
        return r.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> CargoCompany | None:
        r = await self.db.execute(select(CargoCompany).where(CargoCompany.slug == slug))
        return r.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> CargoCompany | None:
        r = await self.db.execute(select(CargoCompany).where(CargoCompany.user_id == user_id))
        return r.scalar_one_or_none()

    async def list_active(self) -> list[CargoCompany]:
        r = await self.db.execute(
            select(CargoCompany).where(CargoCompany.is_active == True)
            .order_by(CargoCompany.company_name)
        )
        return list(r.scalars().all())

    async def list_by_city(self, city: str) -> list[CargoCompany]:
        r = await self.db.execute(
            select(CargoCompany).where(CargoCompany.is_active == True, CargoCompany.city == city)
            .order_by(CargoCompany.company_name)
        )
        return list(r.scalars().all())


class BranchRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoBranch:
        obj = CargoBranch(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoBranch, **kwargs) -> CargoBranch:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, branch_id: int) -> CargoBranch | None:
        r = await self.db.execute(select(CargoBranch).where(CargoBranch.id == branch_id))
        return r.scalar_one_or_none()

    async def list_by_company(self, company_id: int) -> list[CargoBranch]:
        r = await self.db.execute(
            select(CargoBranch).where(CargoBranch.company_id == company_id)
            .order_by(CargoBranch.branch_name)
        )
        return list(r.scalars().all())


class CourierRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoCourier:
        obj = CargoCourier(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoCourier, **kwargs) -> CargoCourier:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, courier_id: int) -> CargoCourier | None:
        r = await self.db.execute(select(CargoCourier).where(CargoCourier.id == courier_id))
        return r.scalar_one_or_none()

    async def list_by_company(self, company_id: int) -> list[CargoCourier]:
        r = await self.db.execute(
            select(CargoCourier).where(CargoCourier.company_id == company_id)
            .order_by(CargoCourier.full_name)
        )
        return list(r.scalars().all())

    async def list_by_branch(self, branch_id: int) -> list[CargoCourier]:
        r = await self.db.execute(
            select(CargoCourier).where(CargoCourier.branch_id == branch_id)
        )
        return list(r.scalars().all())

    async def list_available(self, company_id: int) -> list[CargoCourier]:
        r = await self.db.execute(
            select(CargoCourier).where(
                CargoCourier.company_id == company_id,
                CargoCourier.is_available == True,
                CargoCourier.is_active == True,
            )
        )
        return list(r.scalars().all())


class ShipmentRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoShipment:
        obj = CargoShipment(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoShipment, **kwargs) -> CargoShipment:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, shipment_id: int) -> CargoShipment | None:
        r = await self.db.execute(select(CargoShipment).where(CargoShipment.id == shipment_id))
        return r.scalar_one_or_none()

    async def get_by_tracking(self, tracking_no: str) -> CargoShipment | None:
        r = await self.db.execute(
            select(CargoShipment).where(CargoShipment.tracking_no == tracking_no)
        )
        return r.scalar_one_or_none()

    async def list_by_company(self, company_id: int, status: str = None) -> list[CargoShipment]:
        q = select(CargoShipment).where(CargoShipment.company_id == company_id)
        if status:
            q = q.where(CargoShipment.status == status)
        r = await self.db.execute(q.order_by(CargoShipment.created_at.desc()))
        return list(r.scalars().all())

    async def list_by_sender(self, sender_email: str = None, sender_phone: str = None) -> list[CargoShipment]:
        q = select(CargoShipment)
        if sender_email:
            q = q.where(CargoShipment.sender_email == sender_email)
        if sender_phone:
            q = q.where(CargoShipment.sender_phone == sender_phone)
        r = await self.db.execute(q.order_by(CargoShipment.created_at.desc()))
        return list(r.scalars().all())

    async def list_by_recipient(self, recipient_phone: str = None) -> list[CargoShipment]:
        q = select(CargoShipment).where(CargoShipment.recipient_phone == recipient_phone)
        r = await self.db.execute(q.order_by(CargoShipment.created_at.desc()))
        return list(r.scalars().all())


class TrackingRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoTracking:
        obj = CargoTracking(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def list_by_shipment(self, shipment_id: int) -> list[CargoTracking]:
        r = await self.db.execute(
            select(CargoTracking).where(CargoTracking.shipment_id == shipment_id)
            .order_by(CargoTracking.created_at)
        )
        return list(r.scalars().all())


class PricingRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoPricingTier:
        obj = CargoPricingTier(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoPricingTier, **kwargs) -> CargoPricingTier:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, tier_id: int) -> CargoPricingTier | None:
        r = await self.db.execute(select(CargoPricingTier).where(CargoPricingTier.id == tier_id))
        return r.scalar_one_or_none()

    async def list_by_company(self, company_id: int) -> list[CargoPricingTier]:
        r = await self.db.execute(
            select(CargoPricingTier).where(
                CargoPricingTier.company_id == company_id,
                CargoPricingTier.is_active == True,
            ).order_by(CargoPricingTier.tier_name)
        )
        return list(r.scalars().all())

    async def find_matching(self, company_id: int, weight_kg: float, volume_dm3: float, zone_type: str) -> list[CargoPricingTier]:
        r = await self.db.execute(
            select(CargoPricingTier).where(
                CargoPricingTier.company_id == company_id,
                CargoPricingTier.is_active == True,
                CargoPricingTier.min_weight_kg <= weight_kg,
                (CargoPricingTier.max_weight_kg == None) | (CargoPricingTier.max_weight_kg >= weight_kg),
                CargoPricingTier.min_volume_dm3 <= volume_dm3,
                (CargoPricingTier.max_volume_dm3 == None) | (CargoPricingTier.max_volume_dm3 >= volume_dm3),
                (CargoPricingTier.zone_type == None) | (CargoPricingTier.zone_type == zone_type),
            )
        )
        return list(r.scalars().all())


class ServiceAreaRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoServiceArea:
        obj = CargoServiceArea(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoServiceArea, **kwargs) -> CargoServiceArea:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, area_id: int) -> CargoServiceArea | None:
        r = await self.db.execute(select(CargoServiceArea).where(CargoServiceArea.id == area_id))
        return r.scalar_one_or_none()

    async def list_by_company(self, company_id: int) -> list[CargoServiceArea]:
        r = await self.db.execute(
            select(CargoServiceArea).where(CargoServiceArea.company_id == company_id)
            .order_by(CargoServiceArea.city)
        )
        return list(r.scalars().all())

    async def check_availability(self, company_id: int, city: str, district: str = None) -> CargoServiceArea | None:
        q = select(CargoServiceArea).where(
            CargoServiceArea.company_id == company_id,
            CargoServiceArea.city == city,
            CargoServiceArea.is_available == True,
        )
        if district:
            q = q.where(CargoServiceArea.district == district)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()


class AgreementRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoSellerAgreement:
        obj = CargoSellerAgreement(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: CargoSellerAgreement, **kwargs) -> CargoSellerAgreement:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def get_by_id(self, agreement_id: int) -> CargoSellerAgreement | None:
        r = await self.db.execute(select(CargoSellerAgreement).where(CargoSellerAgreement.id == agreement_id))
        return r.scalar_one_or_none()

    async def get_by_seller_company(self, seller_id: int, company_id: int) -> CargoSellerAgreement | None:
        r = await self.db.execute(
            select(CargoSellerAgreement).where(
                CargoSellerAgreement.seller_id == seller_id,
                CargoSellerAgreement.company_id == company_id,
            )
        )
        return r.scalar_one_or_none()

    async def list_by_seller(self, seller_id: int) -> list[CargoSellerAgreement]:
        r = await self.db.execute(
            select(CargoSellerAgreement).where(
                CargoSellerAgreement.seller_id == seller_id,
                CargoSellerAgreement.is_active == True,
            )
        )
        return list(r.scalars().all())

    async def list_by_company(self, company_id: int) -> list[CargoSellerAgreement]:
        r = await self.db.execute(
            select(CargoSellerAgreement).where(
                CargoSellerAgreement.company_id == company_id,
                CargoSellerAgreement.is_active == True,
            )
        )
        return list(r.scalars().all())

    async def delete(self, agreement_id: int) -> bool:
        r = await self.db.execute(delete(CargoSellerAgreement).where(CargoSellerAgreement.id == agreement_id))
        await self.db.flush()
        return r.rowcount > 0


class ProductShippingRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(self, seller_id: int, product_id: int, company_id: int, **kwargs) -> CargoProductShipping:
        existing = await self.get(seller_id, product_id)
        if existing:
            for k, v in kwargs.items():
                setattr(existing, k, v)
        else:
            existing = CargoProductShipping(seller_id=seller_id, product_id=product_id, company_id=company_id, **kwargs)
            self.db.add(existing)
        await self.db.flush()
        return existing

    async def get(self, seller_id: int, product_id: int) -> CargoProductShipping | None:
        r = await self.db.execute(
            select(CargoProductShipping).where(
                CargoProductShipping.seller_id == seller_id,
                CargoProductShipping.product_id == product_id,
                CargoProductShipping.is_active == True,
            )
        )
        return r.scalar_one_or_none()

    async def list_by_seller(self, seller_id: int) -> list[CargoProductShipping]:
        r = await self.db.execute(
            select(CargoProductShipping).where(
                CargoProductShipping.seller_id == seller_id,
                CargoProductShipping.is_active == True,
            )
        )
        return list(r.scalars().all())

    async def get_by_id(self, shipping_id: int) -> CargoProductShipping | None:
        r = await self.db.execute(select(CargoProductShipping).where(CargoProductShipping.id == shipping_id))
        return r.scalar_one_or_none()


class DeliverySurveyRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoDeliverySurvey:
        obj = CargoDeliverySurvey(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_shipment(self, shipment_id: int) -> CargoDeliverySurvey | None:
        r = await self.db.execute(select(CargoDeliverySurvey).where(CargoDeliverySurvey.shipment_id == shipment_id))
        return r.scalar_one_or_none()

    async def get_by_shipment_user(self, shipment_id: int, user_id: int) -> CargoDeliverySurvey | None:
        r = await self.db.execute(
            select(CargoDeliverySurvey).where(
                CargoDeliverySurvey.shipment_id == shipment_id,
                CargoDeliverySurvey.user_id == user_id,
            )
        )
        return r.scalar_one_or_none()


class ReturnRequestRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> CargoReturnRequest:
        obj = CargoReturnRequest(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_id(self, return_id: int) -> CargoReturnRequest | None:
        r = await self.db.execute(select(CargoReturnRequest).where(CargoReturnRequest.id == return_id))
        return r.scalar_one_or_none()

    async def get_by_shipment(self, shipment_id: int) -> CargoReturnRequest | None:
        r = await self.db.execute(select(CargoReturnRequest).where(CargoReturnRequest.shipment_id == shipment_id))
        return r.scalar_one_or_none()

    async def update(self, obj: CargoReturnRequest, **kwargs) -> CargoReturnRequest:
        for k, v in kwargs.items():
            setattr(obj, k, v)
        await self.db.flush()
        return obj

    async def list_by_user(self, user_id: int) -> list[CargoReturnRequest]:
        r = await self.db.execute(
            select(CargoReturnRequest).where(CargoReturnRequest.user_id == user_id)
            .order_by(CargoReturnRequest.created_at.desc())
        )
        return list(r.scalars().all())
