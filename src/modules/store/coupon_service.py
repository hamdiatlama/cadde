from src.modules.store.models import Coupon
from src.modules.campaign.service import CampaignService


class CouponService:
    def __init__(self, db):
        self.db = db

    async def validate(self, code: str, order_total: float, user_id: int = None) -> dict | None:
        from datetime import datetime, timezone
        from sqlalchemy import select
        r = await self.db.execute(select(Coupon).where(Coupon.code == code, Coupon.is_active == True))
        coupon = r.scalar_one_or_none()
        if not coupon:
            return None
        now = datetime.now(timezone.utc)
        if coupon.expires_at and coupon.expires_at < now:
            return None
        if order_total < coupon.min_order_amount:
            return None
        if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
            return None
        discount = 0
        if coupon.discount_type == "percentage":
            discount = order_total * coupon.discount_value / 100
        elif coupon.discount_type == "fixed":
            discount = min(coupon.discount_value, order_total)
        return {"coupon_id": coupon.id, "code": code, "discount": round(discount, 2),
                "discount_type": coupon.discount_type, "discount_value": coupon.discount_value}

    async def apply(self, code: str, order_total: float, user_id: int = None) -> dict | None:
        result = await self.validate(code, order_total, user_id)
        if not result:
            return None
        from sqlalchemy import update
        from src.modules.store.models import Coupon
        await self.db.execute(
            update(Coupon).where(Coupon.code == code).values(current_uses=Coupon.current_uses + 1)
        )
        return result

    async def create(self, data: dict, admin_id: int) -> dict:
        from datetime import datetime
        coupon = Coupon(
            code=data["code"].upper(), discount_type=data.get("discount_type", "percentage"),
            discount_value=data["discount_value"],
            min_order_amount=data.get("min_order_amount", 0),
            max_uses=data.get("max_uses"), expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
        )
        self.db.add(coupon)
        return {"id": coupon.id, "code": coupon.code, "discount_type": coupon.discount_type,
                "discount_value": coupon.discount_value}

    async def list_all(self):
        from sqlalchemy import select
        r = await self.db.execute(select(Coupon).order_by(Coupon.created_at.desc()))
        coupons = r.scalars().all()
        return [
            {"id": c.id, "code": c.code, "discount_type": c.discount_type,
             "discount_value": c.discount_value, "min_order_amount": c.min_order_amount,
             "current_uses": c.current_uses, "max_uses": c.max_uses,
             "expires_at": c.expires_at.isoformat() if c.expires_at else None,
             "is_active": c.is_active}
            for c in coupons
        ]
