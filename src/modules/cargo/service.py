import uuid, random
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.cargo.repository import (
    CompanyRepo, BranchRepo, CourierRepo, ShipmentRepo,
    TrackingRepo, PricingRepo, ServiceAreaRepo, AgreementRepo,
    ProductShippingRepo, DeliverySurveyRepo, ReturnRequestRepo,
)
from src.modules.cargo.models import (
    CargoCompany, CargoBranch, CargoCourier, CargoShipment,
    CargoPricingTier, CargoServiceArea, CargoSellerAgreement,
    CargoProductShipping, CargoDeliverySurvey, CargoReturnRequest,
    CargoSellerSuspension,
)


class CargoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.companies = CompanyRepo(db)
        self.branches = BranchRepo(db)
        self.couriers = CourierRepo(db)
        self.shipments = ShipmentRepo(db)
        self.tracking = TrackingRepo(db)
        self.pricing = PricingRepo(db)
        self.areas = ServiceAreaRepo(db)
        self.agreements = AgreementRepo(db)
        self.product_shipping = ProductShippingRepo(db)
        self.surveys = DeliverySurveyRepo(db)
        self.returns = ReturnRequestRepo(db)

    async def register(self, user_id: int, data) -> CargoCompany:
        vals = data.model_dump()
        api_key = uuid.uuid4().hex[:32]
        return await self.companies.create(user_id=user_id, api_key=api_key, **vals)

    async def update_company(self, company_id: int, data, user_id: int) -> CargoCompany | None:
        comp = await self.companies.get_by_id(company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.companies.update(comp, **data.model_dump(exclude_none=True))

    async def get_company(self, company_id: int) -> CargoCompany | None:
        return await self.companies.get_by_id(company_id)

    async def get_my_company(self, user_id: int) -> CargoCompany | None:
        return await self.companies.get_by_user(user_id)

    async def list_companies(self, city: str = None) -> list[CargoCompany]:
        if city:
            return await self.companies.list_by_city(city)
        return await self.companies.list_active()

    async def add_branch(self, company_id: int, data, user_id: int) -> CargoBranch | None:
        comp = await self.companies.get_by_id(company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.branches.create(company_id=company_id, **data.model_dump())

    async def update_branch(self, branch_id: int, data, user_id: int) -> CargoBranch | None:
        branch = await self.branches.get_by_id(branch_id)
        if not branch:
            return None
        comp = await self.companies.get_by_id(branch.company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.branches.update(branch, **data.model_dump(exclude_none=True))

    async def list_branches(self, company_id: int) -> list[CargoBranch]:
        return await self.branches.list_by_company(company_id)

    async def add_courier(self, company_id: int, data, user_id: int) -> CargoCourier | None:
        comp = await self.companies.get_by_id(company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.couriers.create(company_id=company_id, **data.model_dump())

    async def update_courier(self, courier_id: int, data, user_id: int) -> CargoCourier | None:
        courier = await self.couriers.get_by_id(courier_id)
        if not courier:
            return None
        comp = await self.companies.get_by_id(courier.company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.couriers.update(courier, **data.model_dump(exclude_none=True))

    async def list_couriers(self, company_id: int) -> list[CargoCourier]:
        return await self.couriers.list_by_company(company_id)

    async def list_available_couriers(self, company_id: int) -> list[CargoCourier]:
        return await self.couriers.list_available(company_id)

    async def create_shipment(self, data, user_id: int = None) -> CargoShipment | None:
        vals = data.model_dump()
        vals["tracking_no"] = "CRG" + uuid.uuid4().hex[:10].upper()
        if vals.get("courier_id"):
            from datetime import datetime
            vals["pickup_confirmed_by_courier"] = True
            vals["pickup_confirmed_at"] = datetime.now().isoformat()
            vals["status"] = "teslim_alindi"
        return await self.shipments.create(**vals)

    async def update_shipment(self, shipment_id: int, data, user_id: int = None) -> CargoShipment | None:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship:
            return None
        vals = data.model_dump(exclude_none=True)
        if "courier_id" in vals and not ship.courier_id and not ship.pickup_confirmed_by_courier:
            from datetime import datetime
            vals["pickup_confirmed_by_courier"] = True
            vals["pickup_confirmed_at"] = datetime.now().isoformat()
            if ship.status == "hazirlaniyor":
                vals["status"] = "teslim_alindi"
        return await self.shipments.update(ship, **vals)

    async def get_shipment(self, shipment_id: int) -> CargoShipment | None:
        return await self.shipments.get_by_id(shipment_id)

    async def get_shipment_by_tracking(self, tracking_no: str) -> CargoShipment | None:
        return await self.shipments.get_by_tracking(tracking_no)

    async def list_company_shipments(self, company_id: int, status: str = None) -> list[CargoShipment]:
        return await self.shipments.list_by_company(company_id, status)

    async def add_tracking(self, shipment_id: int, data) -> dict | None:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship:
            return None
        trk = await self.tracking.create(shipment_id=shipment_id, **data.model_dump())
        await self.shipments.update(ship, status=data.status)
        return {"id": trk.id, "shipment_id": trk.shipment_id, "status": trk.status,
                "location_name": trk.location_name, "notes": trk.notes, "created_by": trk.created_by}

    async def get_tracking(self, shipment_id: int) -> list:
        return await self.tracking.list_by_shipment(shipment_id)

    async def add_pricing(self, company_id: int, data, user_id: int) -> CargoPricingTier | None:
        comp = await self.companies.get_by_id(company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.pricing.create(company_id=company_id, **data.model_dump())

    async def update_pricing(self, tier_id: int, data, user_id: int) -> CargoPricingTier | None:
        tier = await self.pricing.get_by_id(tier_id)
        if not tier:
            return None
        comp = await self.companies.get_by_id(tier.company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.pricing.update(tier, **data.model_dump(exclude_none=True))

    async def list_pricing(self, company_id: int) -> list[CargoPricingTier]:
        return await self.pricing.list_by_company(company_id)

    async def calculate_price(self, company_id: int, weight_kg: float, volume_dm3: float,
                              from_city: str, to_city: str, is_express: bool = False) -> dict | None:
        zone = "sehir_ici" if from_city == to_city else "sehirler_arasi"
        tiers = await self.pricing.find_matching(company_id, weight_kg, volume_dm3, zone)
        if not tiers:
            return None
        tier = tiers[0]
        price = tier.base_price
        price += tier.price_per_kg * weight_kg
        price += tier.price_per_dm3 * volume_dm3
        if tier.fuel_surcharge_percent > 0:
            price += price * (tier.fuel_surcharge_percent / 100)
        if is_express:
            price *= 1.5
        return {"company_id": company_id, "tier_name": tier.tier_name, "base_price": tier.base_price,
                "weight_charge": round(tier.price_per_kg * weight_kg, 2),
                "volume_charge": round(tier.price_per_dm3 * volume_dm3, 2),
                "fuel_surcharge": tier.fuel_surcharge_percent,
                "express_multiplier": 1.5 if is_express else 1.0,
                "total_price": round(price, 2), "currency": "TRY"}

    async def add_service_area(self, company_id: int, data, user_id: int) -> CargoServiceArea | None:
        comp = await self.companies.get_by_id(company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.areas.create(company_id=company_id, **data.model_dump())

    async def update_service_area(self, area_id: int, data, user_id: int) -> CargoServiceArea | None:
        area = await self.areas.get_by_id(area_id)
        if not area:
            return None
        comp = await self.companies.get_by_id(area.company_id)
        if not comp or comp.user_id != user_id:
            return None
        return await self.areas.update(area, **data.model_dump(exclude_none=True))

    async def list_service_areas(self, company_id: int) -> list[CargoServiceArea]:
        return await self.areas.list_by_company(company_id)

    async def add_agreement(self, seller_id: int, data) -> CargoSellerAgreement | None:
        existing = await self.agreements.get_by_seller_company(seller_id, data.company_id)
        if existing:
            return existing
        return await self.agreements.create(seller_id=seller_id, **data.model_dump())

    async def remove_agreement(self, agreement_id: int, seller_id: int) -> bool:
        agreement = await self.agreements.get_by_id(agreement_id)
        if not agreement or agreement.seller_id != seller_id:
            return False
        return await self.agreements.delete(agreement_id)

    async def list_seller_agreements(self, seller_id: int) -> list[dict]:
        agreements = await self.agreements.list_by_seller(seller_id)
        result = []
        for a in agreements:
            comp = await self.companies.get_by_id(a.company_id)
            result.append({"id": a.id, "seller_id": a.seller_id, "company_id": a.company_id,
                           "company_name": comp.company_name if comp else "", "is_preferred": a.is_preferred,
                           "contract_start": a.contract_start, "contract_end": a.contract_end,
                           "negotiated_price_factor": a.negotiated_price_factor, "notes": a.notes, "is_active": a.is_active})
        return result

    async def list_company_agreements(self, company_id: int) -> list[CargoSellerAgreement]:
        return await self.agreements.list_by_company(company_id)

    async def mark_undelivered(self, shipment_id: int, reason: str, branch_id: int, user_id: int) -> dict:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship:
            return {"error": "Gönderi bulunamadı"}
        from datetime import datetime, timedelta
        now = datetime.now()
        attempt = (ship.delivery_attempt_count or 0) + 1
        branch_wait = (now + timedelta(days=2)).isoformat()
        await self.shipments.update(ship, status="subede_bekliyor", delivery_attempt_count=attempt,
            last_delivery_attempt_at=now.isoformat(), undelivered_reason=reason, branch_id=branch_id, branch_wait_until=branch_wait)
        await self.tracking.create(shipment_id=shipment_id, status="subede_bekliyor",
            notes=f"Teslimat başarısız: {reason}. Şubede 2 gün bekletilecek.", created_by="system")
        return {"ok": True, "tracking_no": ship.tracking_no, "status": "subede_bekliyor",
                "branch_wait_until": branch_wait, "delivery_attempt": attempt}

    async def extend_pickup(self, shipment_id: int, user_id: int) -> dict:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship or ship.status != "subede_bekliyor":
            return {"error": "Gönderi şubede beklemiyor"}
        from datetime import datetime, timedelta
        now = datetime.now()
        current_deadline = datetime.fromisoformat(ship.branch_wait_until) if ship.branch_wait_until else now
        if current_deadline < now:
            current_deadline = now
        new_deadline = (current_deadline + timedelta(days=1)).isoformat()
        await self.shipments.update(ship, customer_extended_pickup=True, branch_wait_until=new_deadline, customer_pickup_deadline=new_deadline)
        await self.tracking.create(shipment_id=shipment_id, status="subede_bekliyor",
            notes="Müşteri teslim alacağını bildirdi, süre 1 gün uzatıldı.", created_by="system")
        return {"ok": True, "new_deadline": new_deadline}

    async def auto_return_expired(self, shipment_id: int, product_price: float = 0) -> dict:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship or ship.status != "subede_bekliyor":
            return {"error": "Uygun gönderi değil"}
        from datetime import datetime
        now = datetime.now()
        if ship.branch_wait_until and datetime.fromisoformat(ship.branch_wait_until) > now:
            return {"error": "Bekleme süresi henüz dolmadı"}
        one_way = ship.total_price or 0
        total_paid = product_price + one_way if product_price else one_way * 40
        net_refund = max(0, total_paid - one_way - one_way)
        cargo_earnings = one_way + one_way
        await self.shipments.update(ship, status="iade_ediliyor", refund_amount=total_paid,
            refund_delivery_cost=one_way, refund_return_cost=one_way, refund_net_amount=round(net_refund, 2), refund_processed=False)
        await self.tracking.create(shipment_id=shipment_id, status="iade_ediliyor",
            notes=f"Şubede bekleme süresi doldu, iade ediliyor. İade: {round(net_refund,2)} TL (kesinti: {cargo_earnings:.0f} TL kargoya)", created_by="system")
        return {"ok": True, "tracking_no": ship.tracking_no, "status": "iade_ediliyor",
                "refund": {"total_paid": total_paid, "product_price": product_price or (total_paid - one_way),
                           "delivery_cost": one_way, "return_cost": one_way, "cargo_total": cargo_earnings, "net_refund": round(net_refund, 2)}}

    async def set_product_shipping(self, seller_id: int, data) -> CargoProductShipping:
        vals = data.model_dump()
        product_id = vals.pop("product_id")
        company_id = vals.pop("company_id")
        return await self.product_shipping.upsert(seller_id, product_id, company_id, **vals)

    async def get_product_shipping(self, seller_id: int, product_id: int) -> CargoProductShipping | None:
        return await self.product_shipping.get(seller_id, product_id)

    async def list_my_product_shipping(self, seller_id: int) -> list[CargoProductShipping]:
        return await self.product_shipping.list_by_seller(seller_id)

    async def generate_delivery_code(self, shipment_id: int) -> str | None:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship:
            return None
        code = str(random.randint(100000, 999999))
        await self.shipments.update(ship, delivery_code=code)
        return code

    async def confirm_delivery(self, delivery_code: str, note: str = None) -> dict:
        r = await self.db.execute(select(CargoShipment).where(CargoShipment.delivery_code == delivery_code))
        ship = r.scalar_one_or_none()
        if not ship:
            return {"error": "Geçersiz teslimat kodu"}
        from datetime import datetime
        now = datetime.now().isoformat()
        await self.shipments.update(ship, status="teslim_edildi", actual_delivery_date=now,
            delivery_confirmed_by_recipient=True, delivery_confirmed_at=now, delivery_note=note)
        await self.tracking.create(shipment_id=ship.id, status="teslim_edildi", notes=note or "Teslimat gerçekleşti", created_by="system")
        return {"ok": True, "tracking_no": ship.tracking_no, "status": "teslim_edildi"}

    async def reject_delivery(self, delivery_code: str, note: str = None) -> dict:
        r = await self.db.execute(select(CargoShipment).where(CargoShipment.delivery_code == delivery_code))
        ship = r.scalar_one_or_none()
        if not ship:
            return {"error": "Geçersiz teslimat kodu"}
        await self.shipments.update(ship, status="iade_edildi", delivery_note=note)
        await self.tracking.create(shipment_id=ship.id, status="iade_edildi", notes=note or "Alıcı teslim almayı reddetti", created_by="system")
        return {"ok": True, "tracking_no": ship.tracking_no, "status": "iade_edildi"}

    async def submit_survey(self, shipment_id: int, user_id: int, data) -> CargoDeliverySurvey | None:
        existing = await self.surveys.get_by_shipment_user(shipment_id, user_id)
        if existing:
            return None
        return await self.surveys.create(shipment_id=shipment_id, user_id=user_id, **data.model_dump())

    async def get_survey(self, shipment_id: int) -> CargoDeliverySurvey | None:
        return await self.surveys.get_by_shipment(shipment_id)

    async def _check_buyer_fraud(self, user_id: int) -> dict:
        from datetime import datetime, timedelta
        month_ago = (datetime.now() - timedelta(days=30)).isoformat()
        r = await self.db.execute(select(CargoReturnRequest).where(CargoReturnRequest.user_id == user_id, CargoReturnRequest.created_at >= month_ago))
        recent = len(list(r.scalars().all()))
        r = await self.db.execute(select(CargoReturnRequest).where(CargoReturnRequest.user_id == user_id))
        total = len(list(r.scalars().all()))
        return {"recent_30_days": recent, "total_returns": total, "is_suspicious": recent >= 3 or total >= 5, "is_blocked": total >= 8}

    async def _check_seller_fraud(self, company_id: int) -> dict:
        from datetime import datetime, timedelta
        year_ago = (datetime.now() - timedelta(days=365)).isoformat()
        r = await self.db.execute(
            select(CargoReturnRequest).where(
                CargoReturnRequest.liability_party == "cargo",
                CargoReturnRequest.created_at >= year_ago,
            )
        )
        all_claims = list(r.scalars().all())
        company_count = 0
        for claim in all_claims:
            ship = await self.shipments.get_by_id(claim.shipment_id)
            if ship and ship.company_id == company_id:
                company_count += 1
        return {"yearly_damage_claims": company_count, "is_suspicious": company_count >= 2, "seller_liable": company_count >= 3}

    async def _apply_seller_suspension(self, seller_id: int) -> dict:
        """Satıcıya kademeli ceza uygula: 3g → 10g → 3ay → 1yıl"""
        r = await self.db.execute(
            select(CargoSellerSuspension).where(
                CargoSellerSuspension.seller_id == seller_id,
                CargoSellerSuspension.is_active == True,
            ).order_by(CargoSellerSuspension.offense_count.desc())
        )
        last = r.scalar_one_or_none()
        offense = (last.offense_count + 1) if last else 1
        from datetime import datetime, timedelta
        days_map = {1: 3, 2: 10, 3: 90, 4: 365}
        days = days_map.get(offense, 365)
        end_date = (datetime.now() + timedelta(days=days)).isoformat()
        susp = CargoSellerSuspension(
            seller_id=seller_id, offense_count=offense,
            suspension_days=days, end_date=end_date,
            reason=f"{offense}. kez hasarlı gönderi tespiti. {days} gün askıya alma.",
        )
        self.db.add(susp)
        await self.db.flush()
        return {"offense": offense, "suspension_days": days, "end_date": end_date,
                "message": f"Satışlarınız {days} gün süreyle askıya alınmıştır. "
                           f"({offense}. ihlal). Hesabınız {end_date} tarihine kadar pasiftir."}

    async def check_seller_suspension(self, seller_id: int) -> dict | None:
        from datetime import datetime
        r = await self.db.execute(
            select(CargoSellerSuspension).where(
                CargoSellerSuspension.seller_id == seller_id,
                CargoSellerSuspension.is_active == True,
            ).order_by(CargoSellerSuspension.end_date.desc())
        )
        active = r.scalar_one_or_none()
        if not active:
            return None
        now = datetime.now().isoformat()
        if active.end_date < now:
            await self.db.execute(
                update(CargoSellerSuspension).where(CargoSellerSuspension.id == active.id).values(is_active=False)
            )
            await self.db.flush()
            return None
        days_left = (datetime.fromisoformat(active.end_date) - datetime.now()).days
        return {"is_suspended": True, "offense_count": active.offense_count,
                "suspension_days": active.suspension_days, "end_date": active.end_date,
                "days_left": days_left,
                "message": f"Gönderdiğiniz ürünlerde kırık ürünler sebebiyle satışlarınız askıya alınmıştır. "
                           f"Hesabınız {days_left} gün daha askıda ({active.offense_count}. ihlal)."}

    async def create_return_request(self, shipment_id: int, user_id: int, data) -> dict:
        ship = await self.shipments.get_by_id(shipment_id)
        if not ship:
            return {"error": "Gönderi bulunamadı"}
        buyer_fraud = await self._check_buyer_fraud(user_id)
        if buyer_fraud["is_blocked"]:
            return {"error": "Hesabınızda çok sayıda iade talebi bulunduğu için işlem reddedildi.",
                    "fraud_status": "blocked", "total_returns": buyer_fraud["total_returns"]}
        seller_fraud = await self._check_seller_fraud(ship.company_id)
        from datetime import datetime, timedelta
        is_within = False
        if ship.delivery_confirmed_at:
            delivered = datetime.fromisoformat(ship.delivery_confirmed_at)
            is_within = (datetime.now() - delivered).total_seconds() / 60 <= 30
        existing = await self.returns.get_by_shipment(shipment_id)
        if existing:
            return {"error": "Bu gönderi için zaten iade talebi var"}
        vals = data.model_dump()
        liability_party = None
        liable_amount = 0
        replacement = False
        reason_lower = (vals.get("reason") or "").lower()
        defective_keywords = ["defolu", "defo", "hasarli", "hasar", "kirik", "kırık", "calismiyor",
                              "çalışmıyor", "tarihi gecmis", "tarihi geçmiş", "bozuk", "eksik",
                              "yanlis", "yanlış", "hatali", "hatalı", "süresi dolmus", "süresi dolmuş"]
        is_product_defect = any(k in reason_lower for k in defective_keywords)
        if ship.pickup_confirmed_by_courier and (vals.get("is_package_damaged") or vals.get("package_condition") == "hasarli"):
            if seller_fraud["seller_liable"]:
                liability_party = "seller"
                liable_amount = ship.total_price or 0
            else:
                liability_party = "cargo"
                liable_amount = ship.total_price or 0
                replacement = True
        elif is_product_defect:
            liability_party = "seller"
            liable_amount = ship.total_price or 0
        req = await self.returns.create(shipment_id=shipment_id, user_id=user_id, is_within_window=is_within,
            liability_party=liability_party, liable_amount=liable_amount, replacement_required=replacement, **vals)
        await self.shipments.update(ship, status="iade_talebi_inceleniyor" if buyer_fraud["is_suspicious"] else "iade_talebi")
        result = {"id": req.id, "shipment_id": req.shipment_id, "reason": req.reason, "status": req.status,
                  "is_within_window": is_within, "fraud_warning": buyer_fraud["is_suspicious"],
                  "total_returns": buyer_fraud["total_returns"]}
        if liability_party == "cargo":
            result["liability"] = {"party": "cargo", "note": "Kargo firması hasardan sorumlu. Tam iade + ücretsiz yeni gönderim.",
                                   "refund_type": "full", "liable_amount": liable_amount, "replacement_free": True}
        elif liability_party == "seller":
            result["liability"] = {"party": "seller", "note": f"Satıcının {seller_fraud['yearly_damage_claims']}. hasarlı gönderisi. Sorumluluk satıcıya ait.",
                                   "refund_type": "seller_pays", "seller_claims": seller_fraud["yearly_damage_claims"]}
            # Satıcıya ceza uygula
            seller_ship = await self.shipments.get_by_id(shipment_id)
            if seller_ship:
                r = await self.db.execute(select(CargoCompany).where(CargoCompany.id == seller_ship.company_id))
                cargo_comp = r.scalar_one_or_none()
                if cargo_comp:
                    r = await self.db.execute(select(CargoSellerAgreement).where(CargoSellerAgreement.company_id == cargo_comp.id))
                    agreements = list(r.scalars().all())
                    for ag in agreements:
                        suspension = await self._apply_seller_suspension(ag.seller_id)
                        result["seller_suspension"] = suspension
        if seller_fraud["is_suspicious"]:
            result["seller_fraud_warning"] = True
            result["seller_yearly_claims"] = seller_fraud["yearly_damage_claims"]
        return result

    async def get_return_request(self, shipment_id: int) -> dict | None:
        req = await self.returns.get_by_shipment(shipment_id)
        if not req:
            return None
        return {"id": req.id, "shipment_id": req.shipment_id, "reason": req.reason, "description": req.description,
                "evidence_photos": req.evidence_photos, "evidence_videos": req.evidence_videos, "status": req.status,
                "is_within_window": req.is_within_window, "resolution": req.resolution}

    async def list_company_claims(self, company_id: int, user_id: int) -> list[dict]:
        comp = await self.companies.get_by_id(company_id)
        if not comp or comp.user_id != user_id:
            return []
        result = []
        for ship in await self.shipments.list_by_company(company_id):
            req = await self.returns.get_by_shipment(ship.id)
            survey = await self.surveys.get_by_shipment(ship.id)
            if req or (survey and (survey.is_package_damaged or survey.is_package_opened)):
                result.append({"shipment_id": ship.id, "tracking_no": ship.tracking_no, "recipient_name": ship.recipient_name,
                               "status": ship.status, "is_fragile": ship.is_fragile, "pickup_confirmed": ship.pickup_confirmed_by_courier,
                               "return_request": {"id": req.id, "reason": req.reason, "status": req.status, "is_within_window": req.is_within_window,
                                                   "liability_party": req.liability_party, "liable_amount": req.liable_amount} if req else None,
                               "survey": {"package_condition": survey.package_condition, "is_package_damaged": survey.is_package_damaged,
                                           "is_package_opened": survey.is_package_opened, "satisfaction_score": survey.satisfaction_score} if survey else None})
        return result
